import sys
from datetime import datetime
from config import settings
from models import SessionState, AgentAction
from memory import SessionMemoryManager
from scanner import NetworkScanner
from agent import CyberGuardAgent

# Import core tools
from tools.banner_grab import grab_banner
from tools.cve_lookup import lookup_cve
from tools.exploit_suggest import suggest_exploit

# Import Rich components for elite CLI UX
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

console = Console()

def run_autonomous_assessment(target: str, max_turns: int = 5):
    """
    Orchestrates the entire end-to-end lifecycle of CyberGuard AI with an enhanced Rich CLI view.
    """
    session_id = f"cg-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    
    # Render a beautiful tool banner
    console.print(Panel.fit(
        f"[bold cyan]CyberGuard AI — Autonomous Penetration Testing Agent[/bold cyan]\n"
        f"[bold white]Session ID:[/bold white] [yellow]{session_id}[/yellow] | [bold white]Target Scoped:[/bold white] [green]{target}[/green]",
        border_style="magenta"
    ))

    memory_mgr = SessionMemoryManager(session_id=session_id, target=target)
    session_state = memory_mgr.load_session()
    
    # 1. Active Scan Phase with a live text status spinner
    with console.status(f"[bold yellow]Running initial sensory Nmap scan on target {target}...[/bold yellow]", spinner="bouncingBar"):
        scanner = NetworkScanner(target=target)
        scan_results = scanner.run_port_scan(ports="21,22,80,443,8080")
    
    session_state.discovered_host_info = scan_results
    memory_mgr.save_session(session_state)
    
    if scan_results.status == "down" or not scan_results.open_ports:
        console.print(f"[bold red][!] Target host appears down or completely closed. Generating quick exit report...[/bold red]")
        from reporter import SecurityReporter
        SecurityReporter(session_state).generate_markdown_report()
        return

    # Render a clean table of discovered ports immediately
    port_table = Table(title="Exposed Attack Surface Discovery", title_style="bold cyan")
    port_table.add_column("Port", style="yellow")
    port_table.add_column("Protocol", style="green")
    port_table.add_column("State", style="bold red")
    port_table.add_column("Identified Service", style="white")
    
    for port in scan_results.open_ports:
        port_table.add_row(str(port.port), port.protocol.upper(), port.state, port.service)
    console.print(port_table)

    # 2. Wire up the AI Core Agent
    agent = CyberGuardAgent(target=target)
    agent.register_tool("grab_banner", grab_banner)
    agent.register_tool("lookup_cve", lookup_cve)
    agent.register_tool("suggest_exploit", suggest_exploit)

    console.print(f"\n[bold green][+][/bold green] Operational tools safely linked to Gemini Brain framework.\n")

    # 3. Autonomous Execution Loop
    turn = 0
    while turn < max_turns:
        turn += 1
        console.print(f"\n[bold magenta]====== Autonomous Turn {turn} of {max_turns} ======[/bold magenta]")
        
        with console.status("[bold cyan]Agent is analyzing logs and calculating next move via Gemini API...[/bold cyan]", spinner="dots"):
            proposed_action = agent.run_reasoning_step(session_state)
            
        if not proposed_action:
            console.print("[bold green][✓] Brain indicated assessment completeness. Ending execution loop.[/bold green]")
            break
            
        tool_name = proposed_action.tool_name
        tool_args = proposed_action.arguments
        
        console.print(f"[bold yellow][➔] Brain Decision:[/bold yellow] Invoke tool [bold green]'{tool_name}'[/bold green] on arguments [cyan]{tool_args}[/cyan]")
        
        # Tool routing and execution handler
        if tool_name in agent.tool_registry:
            try:
                execution_func = agent.tool_registry[tool_name]
                
                with console.status(f"[bold red]Executing functional hardware tool: {tool_name}...[/bold red]", spinner="binary"):
                    if tool_name == "grab_banner":
                        p = int(tool_args.get("port", 22))
                        raw_result = execution_func(target=target, port=p)
                    elif tool_name == "lookup_cve":
                        cve = str(tool_args.get("cve_id", ""))
                        raw_result = execution_func(cve_id=cve)
                    elif tool_name == "suggest_exploit":
                        summary = str(tool_args.get("service_summary", "Generic endpoint"))
                        raw_result = execution_func(service_summary=summary)
                    else:
                        raw_result = "Configuration mismatched."

                proposed_action.result_summary = raw_result
                console.print(Panel(f"[dim white]{raw_result.strip()}[/dim white]", title=f"Result Extract: {tool_name}", border_style="green"))

                if tool_name == "grab_banner" and "Error" not in raw_result:
                    session_state.findings_summary.append(f"Successfully grabbed banner on port {tool_args.get('port')}: {raw_result}")

            except Exception as e:
                proposed_action.result_summary = f"Execution error: {str(e)}"
                console.print(f"[bold red][!] Tool crashed during execution: {e}[/bold red]")
        else:
            proposed_action.result_summary = f"Error: Tool '{tool_name}' is not registered."
            console.print(f"[bold red][!] Attempted to run unregistered tool: {tool_name}[/bold red]")

        session_state.actions_taken.append(proposed_action)
        memory_mgr.save_session(session_state)

    # 4. Compile the Final Asset Document
    console.print("\n" + "="*60)
    with console.status("[bold green]Compiling professional security audit report...[/bold green]", spinner="aesthetic"):
        from reporter import SecurityReporter
        final_report_path = SecurityReporter(session_state).generate_markdown_report()
        
    console.print(Panel(
        f"[bold green][✓] Process Complete![/bold green]\n"
        f"Final Open-Source Report generated successfully at:\n"
        f"[bold yellow]{final_report_path}[/bold yellow]",
        title="Report Finalized", border_style="cyan"
    ))

if __name__ == "__main__":
    target_to_test = sys.argv[1] if len(sys.argv) > 1 else settings.DEFAULT_TARGET
    run_autonomous_assessment(target=target_to_test)