#!/usr/bin/env python3
"""
YuHun CLI v0.1
==============
Unified command-line interface for the ToneSoul/YuHun system.

This CLI demonstrates the full World Model × Mind Model architecture:
- Multi-Path cognitive reasoning (5 pathways)
- RAG-based verification
- Decision Kernel integration
- StepLedger traceability

Usage:
    python yuhun_cli.py                    # Interactive mode
    python yuhun_cli.py "Your question"    # Single query mode
    python yuhun_cli.py --demo             # Run demo scenarios

Author: Antigravity + 黃梵威
Date: 2025-12-08
"""

import sys
import os
import argparse
from datetime import datetime

# Setup paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, 'body'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'core'))

# ASCII Art Banner
BANNER = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗   ██╗██╗   ██╗██╗  ██╗██╗   ██╗███╗   ██╗              ║
║   ╚██╗ ██╔╝██║   ██║██║  ██║██║   ██║████╗  ██║              ║
║    ╚████╔╝ ██║   ██║███████║██║   ██║██╔██╗ ██║              ║
║     ╚██╔╝  ██║   ██║██╔══██║██║   ██║██║╚██╗██║              ║
║      ██║   ╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║              ║
║      ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝              ║
║                                                              ║
║              語魂 · World Model × Mind Model                 ║
║                                                              ║
║   "別人給 AGI 眼睛；我們給 AGI 靈魂。"                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════
# Component Loading
# ═══════════════════════════════════════════════════════════════════════════

class YuHunCLI:
    """Main CLI class integrating all YuHun components."""
    
    def __init__(self, model: str = "gemma3:4b", verbose: bool = True):
        self.model = model
        self.verbose = verbose
        self.components = {}
        
        self._load_components()
    
    def _log(self, msg: str):
        if self.verbose:
            print(f"[YuHun] {msg}")
    
    def _load_components(self):
        """Load all available components."""
        
        # Multi-Path Engine
        try:
            from multipath_engine import MultiPathEngine
            self.components['multipath'] = MultiPathEngine(model=self.model)
            self._log("✅ Multi-Path Engine loaded")
        except Exception as e:
            self._log(f"⚠️ Multi-Path Engine: {e}")
        
        # Verification Bridge
        try:
            from verification_bridge import VerificationBridge
            self.components['verification'] = VerificationBridge()
            self._log("✅ Verification Bridge loaded")
        except Exception as e:
            self._log(f"⚠️ Verification Bridge: {e}")
        
        # Decision Kernel
        try:
            from decision_kernel import DecisionKernel, create_decision_kernel
            self.components['decision'] = create_decision_kernel()
            self._log("✅ Decision Kernel loaded")
        except Exception as e:
            self._log(f"⚠️ Decision Kernel: {e}")
        
        # StepLedger
        try:
            from step_ledger import StepLedger
            ledger_path = os.path.join(ROOT_DIR, 'memory', 'yuhun_cli_ledger.jsonl')
            self.components['ledger'] = StepLedger(storage_path=ledger_path)
            self._log("✅ StepLedger loaded")
        except Exception as e:
            self._log(f"⚠️ StepLedger: {e}")
    
    def process(self, user_input: str) -> dict:
        """
        Process user input through the full YuHun pipeline.
        
        Returns:
            dict with response, metrics, and trace
        """
        result = {
            'input': user_input,
            'timestamp': datetime.now().isoformat(),
            'response': None,
            'poav': None,
            'gate': None,
            'verification': None,
            'pathways': {},
            'trace': []
        }
        
        # Step 1: Multi-Path Processing
        if 'multipath' in self.components:
            result['trace'].append("Running Multi-Path...")
            try:
                mp_result = self.components['multipath'].run_minimal(user_input)
                result['response'] = mp_result.synthesis
                result['poav'] = mp_result.poav_score
                result['gate'] = mp_result.gate_decision
                
                for ptype, presult in mp_result.pathway_results.items():
                    result['pathways'][ptype.value] = presult.content[:200]
                
                result['trace'].append(f"POAV={result['poav']:.3f}, Gate={result['gate']}")
            except Exception as e:
                result['trace'].append(f"Multi-Path error: {e}")
        
        # Step 2: Verification (if response exists)
        if 'verification' in self.components and result['response']:
            result['trace'].append("Running Verification...")
            try:
                report = self.components['verification'].verify_response(result['response'])
                result['verification'] = {
                    'fabrication_risk': report.fabrication_risk,
                    'entities_count': len(report.entities_found),
                    'high_risk': report.high_risk_entities
                }
                result['trace'].append(f"Fabrication Risk={report.fabrication_risk:.2f}")
            except Exception as e:
                result['trace'].append(f"Verification error: {e}")
        
        # Step 3: Log to StepLedger
        if 'ledger' in self.components:
            try:
                from step_ledger import Event
                event = Event(
                    event_type="yuhun_response",
                    content=user_input[:100],
                    semantic_state={
                        'poav': result.get('poav'),
                        'gate': result.get('gate'),
                        'verification': result.get('verification')
                    }
                )
                self.components['ledger'].record(event)
                result['trace'].append("Logged to StepLedger")
            except Exception as e:
                result['trace'].append(f"Ledger error: {e}")
        
        return result
    
    def format_response(self, result: dict) -> str:
        """Format result for display."""
        lines = []
        lines.append("")
        lines.append("─" * 60)
        
        # Response
        if result['response']:
            lines.append("📝 Response:")
            lines.append(result['response'][:500])
            if len(result['response']) > 500:
                lines.append("... (truncated)")
        
        lines.append("")
        lines.append("─" * 60)
        
        # Metrics
        lines.append("📊 Metrics:")
        if result['poav'] is not None:
            poav_bar = "█" * int(result['poav'] * 10) + "░" * (10 - int(result['poav'] * 10))
            lines.append(f"   POAV: [{poav_bar}] {result['poav']:.3f}")
        
        if result['gate']:
            gate_emoji = {"pass": "✅", "rewrite": "⚠️", "block": "❌"}.get(result['gate'], "❓")
            lines.append(f"   Gate: {gate_emoji} {result['gate'].upper()}")
        
        if result['verification']:
            v = result['verification']
            risk_emoji = "🔴" if v['fabrication_risk'] >= 0.7 else "🟡" if v['fabrication_risk'] >= 0.4 else "🟢"
            lines.append(f"   Verification: {risk_emoji} Risk={v['fabrication_risk']:.2f}")
        
        lines.append("")
        lines.append("─" * 60)
        
        # Pathways (abbreviated)
        if result['pathways']:
            lines.append("🧠 Pathways:")
            for name, content in list(result['pathways'].items())[:3]:
                lines.append(f"   {name}: {content[:60]}...")
        
        lines.append("─" * 60)
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Demo Mode
# ═══════════════════════════════════════════════════════════════════════════

DEMO_PROMPTS = [
    "什麼是語魂？它和普通 AI 有什麼不同？",
    "如何判斷一個 AI 的回答是否可信？",
    "Dr. James Thornberry 在 1987 年發現了什麼？",  # Fabrication test
]


def run_demo(cli: YuHunCLI):
    """Run demo scenarios."""
    print("\n🎯 Demo Mode: Testing 3 Scenarios\n")
    
    for i, prompt in enumerate(DEMO_PROMPTS, 1):
        print(f"{'═' * 60}")
        print(f"Demo {i}/{len(DEMO_PROMPTS)}")
        print(f"Prompt: {prompt}")
        
        result = cli.process(prompt)
        print(cli.format_response(result))
        print()


# ═══════════════════════════════════════════════════════════════════════════
# Interactive Mode
# ═══════════════════════════════════════════════════════════════════════════

def run_interactive(cli: YuHunCLI):
    """Run interactive REPL."""
    print("\n🔮 Interactive Mode")
    print("   Type your question and press Enter.")
    print("   Commands: /quit, /status, /help")
    print()
    
    while True:
        try:
            user_input = input("You> ").strip()
            
            if not user_input:
                continue
            
            # Commands
            if user_input.startswith('/'):
                cmd = user_input.lower()
                
                if cmd in ['/quit', '/exit', '/q']:
                    print("👋 Goodbye!")
                    break
                
                elif cmd == '/status':
                    print(f"Components loaded: {list(cli.components.keys())}")
                    continue
                
                elif cmd == '/help':
                    print("Commands:")
                    print("  /quit   - Exit")
                    print("  /status - Show loaded components")
                    print("  /help   - Show this help")
                    continue
                
                else:
                    print(f"Unknown command: {cmd}")
                    continue
            
            # Process query
            print("\n⏳ Processing...")
            result = cli.process(user_input)
            print(cli.format_response(result))
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            break


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="YuHun CLI - World Model × Mind Model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python yuhun_cli.py                     # Interactive mode
  python yuhun_cli.py "What is YuHun?"    # Single query
  python yuhun_cli.py --demo              # Run demos
        """
    )
    
    parser.add_argument('query', nargs='?', help='Query to process')
    parser.add_argument('--demo', action='store_true', help='Run demo scenarios')
    parser.add_argument('--model', default='gemma3:4b', help='LLM model to use')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress loading messages')
    
    args = parser.parse_args()
    
    # Banner
    print(BANNER)
    
    # Initialize
    cli = YuHunCLI(model=args.model, verbose=not args.quiet)
    
    print(f"\n📍 Model: {args.model}")
    print(f"📍 Components: {len(cli.components)}")
    
    # Mode selection
    if args.demo:
        run_demo(cli)
    elif args.query:
        result = cli.process(args.query)
        print(cli.format_response(result))
    else:
        run_interactive(cli)


if __name__ == "__main__":
    main()
