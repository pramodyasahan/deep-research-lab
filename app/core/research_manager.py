from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
import asyncio

class ResearchManager:

    async def run(self, query: str) -> list[str]:
        """ Run the deep research process, collecting status messages and the final report. """
        trace_id = gen_trace_id()
        statuses: list[str] = []

        # Initial trace link
        link = f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
        print(link)
        statuses.append(link)

        # Start research
        msg = "Starting research..."
        print(msg)
        statuses.append(msg)

        # Plan and perform searches
        search_plan = await self.plan_searches(query)
        msg = "Searches planned, starting to search..."
        print(msg)
        statuses.append(msg)

        search_results = await self.perform_searches(search_plan)
        msg = "Searches complete, writing report..."
        print(msg)
        statuses.append(msg)

        # Write and send report
        report = await self.write_report(query, search_results)
        msg = "Report written, sending email..."
        print(msg)
        statuses.append(msg)

        await self.send_email(report)
        msg = "Email sent, research complete"
        print(msg)
        statuses.append(msg)

        # Append the final report text
        statuses.append(report.markdown_report)
        return statuses

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches according to the plan """
        print("Searching...")
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results: list[str] = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str:
        """ Perform a single search for the query """
        prompt = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                prompt,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("Writing report...")
        prompt = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            prompt,
        )
        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        """ Send the final report via email """
        print("Sending email...")
        await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
