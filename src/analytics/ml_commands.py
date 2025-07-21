
#!/usr/bin/env python3
"""
Machine Learning Commands for Trading Bot
Run ML analysis and get trade recommendations
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.analytics.ml_analyzer import ml_analyzer
from src.analytics.trade_logger import trade_logger
from src.analytics.daily_reporter import DailyReporter
from src.reporting.telegram_reporter import TelegramReporter
from datetime import datetime, timedelta

def train_ml_models():
    """Train ML models on historical data"""
    print("🤖 Training ML models...")
    results = ml_analyzer.train_models()

    if "error" in results:
        print(f"❌ Error: {results['error']}")
    else:
        print("✅ ML models trained successfully!")
        print(f"📊 Profitability accuracy: {results.get('profitability_accuracy', 'N/A'):.2%}")
        print(f"📈 PnL R² score: {results.get('pnl_r2_score', 'N/A'):.2f}")
        print(f"⏱️ Duration R² score: {results.get('duration_r2_score', 'N/A'):.2f}")

        if 'profitability_features' in results:
            print("\n🔍 Top features for profitability:")
            for feature, importance in results['profitability_features'][:5]:
                print(f"  {feature}: {importance:.3f}")

def generate_insights():
    """Generate trading insights"""
    print("📊 Generating trading insights...")
    insights = ml_analyzer.generate_insights()

    if "error" in insights:
        print(f"❌ Error: {insights['error']}")
    else:
        print("✅ Insights generated successfully!")

        # Strategy performance
        if 'strategy_performance' in insights:
            print("\n🎯 Strategy Performance:")
            for strategy, stats in insights['strategy_performance'].items():
                print(f"  {strategy}: Win Rate {stats['was_profitable']['mean']:.2%}")

        # Time analysis
        if 'time_analysis' in insights:
            print("\n⏰ Best Trading Hours:")
            for hour, win_rate in insights['time_analysis']['best_trading_hours'].items():
                print(f"  {hour}:00 - {win_rate:.2%} win rate")

def test_prediction():
    """Test ML prediction with sample data"""
    print("🔮 Testing ML prediction...")

    # Sample trade features
    sample_features = {
        'strategy': 'rsi_oversold',
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'leverage': 5,
        'position_size_usdt': 100,
        'rsi_entry': 25,  # Oversold
        'macd_entry': -0.5,
        'hour_of_day': 14,  # London-NY overlap
        'day_of_week': 2,   # Wednesday
        'month': 12,
        'market_trend': 'BULLISH',
        'volatility_score': 0.3,
        'signal_strength': 0.8
    }

    prediction = ml_analyzer.predict_trade_outcome(sample_features)

    if "error" in prediction:
        print(f"❌ Error: {prediction['error']}")
    else:
        print("✅ Prediction generated!")
        print(f"📈 Profit probability: {prediction.get('profit_probability', 0):.2%}")
        print(f"💰 Predicted PnL: {prediction.get('predicted_pnl_percentage', 0):.2f}%")
        print(f"⏱️ Predicted duration: {prediction.get('predicted_duration_minutes', 0):.0f} minutes")
        print(f"🎯 Recommendation: {prediction.get('recommendation', 'UNKNOWN')}")
        print(f"🔮 Confidence: {prediction.get('confidence', 0):.2%}")

def send_manual_report():
    """Send manual daily report"""
    print("📊 Sending manual daily report...")

    # Initialize telegram reporter
    from src.config.global_config import global_config
    telegram_reporter = TelegramReporter()
    daily_reporter = DailyReporter(telegram_reporter)

    # Send report for yesterday
    yesterday = datetime.now() - timedelta(days=1)
    success = daily_reporter.send_manual_report(yesterday)

    if success:
        print("✅ Daily report sent successfully!")
    else:
        print("❌ Failed to send daily report")

def export_data():
    """Export trade data for external analysis"""
    print("📤 Exporting trade data...")

    filename = trade_logger.export_for_ml()
    if filename:
        print(f"✅ Data exported to: {filename}")
    else:
        print("❌ No data to export")

def run_parameter_optimization():
    """Run parameter optimization simulation"""
    print("🔧 Running parameter optimization...")
    from src.analytics.trade_logger import trade_logger
    
    closed_trades = [t for t in trade_logger.trades if t.trade_status == "CLOSED"]
    if len(closed_trades) < 5:
        print("❌ Need at least 5 closed trades for optimization")
        return
    
    results = ml_analyzer.simulate_parameter_optimization(closed_trades)
    
    if results:
        print("✅ Optimization complete!")
        for scenario_type, data in results.items():
            print(f"\n🎯 {scenario_type.upper()}:")
            print(f"  Average improvement: {data['avg_improvement']:.2f}%")
            print(f"  Best improvement: {data['best_improvement']:.2f}%")
            
            # Show best parameters
            best_params = data['parameters']
            for key, value in best_params.items():
                if key not in ['scenario_type']:
                    print(f"  Optimal {key}: {value}")
    else:
        print("❌ No optimization results generated")

def get_ai_insights():
    """Get insights from external AI advisor"""
    print("🤖 Getting AI advisor insights...")
    
    # Check if API key is set
    api_key = input("Enter OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️ Skipping AI insights - no API key provided")
        print("💡 To enable AI insights, get an API key from OpenAI, Claude, or Gemini")
        return
    
    try:
        from src.analytics.ai_advisor import ai_advisor
        
        # Set API key
        ai_advisor.set_api_key('openai', api_key)
        
        # Prepare context
        context = ml_analyzer.prepare_ai_context()
        
        # Get AI analysis (mock for now)
        import asyncio
        
        async def get_analysis():
            return await ai_advisor.analyze_trading_performance(context)
        
        response = asyncio.run(get_analysis())
        
        if response.get('success'):
            analysis = response['analysis']
            
            print("\n🎯 AI PERFORMANCE ASSESSMENT:")
            perf = analysis['performance_assessment']
            print(f"  Overall Rating: {perf['overall_rating']}")
            print(f"  Trend: {perf['profitability_trend']}")
            
            print("\n💪 KEY STRENGTHS:")
            for strength in perf['key_strengths']:
                print(f"  ✅ {strength}")
            
            print("\n⚠️ AREAS FOR IMPROVEMENT:")
            for weakness in perf['main_weaknesses']:
                print(f"  📋 {weakness}")
            
            print("\n🔧 IMMEDIATE ACTIONS:")
            for action in analysis['optimization_recommendations']['immediate_actions']:
                print(f"  🎯 {action}")
            
            print("\n💡 TECHNICAL IMPROVEMENTS:")
            for improvement in analysis['technical_improvements']['ml_enhancements']:
                print(f"  🚀 {improvement}")
                
        else:
            print(f"❌ AI analysis failed: {response.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error getting AI insights: {e}")

def analyze_what_if_scenarios():
    """Analyze what-if scenarios for trade optimization"""
    print("🔮 Analyzing what-if scenarios...")
    
    # Get a recent trade for analysis
    from src.analytics.trade_logger import trade_logger
    closed_trades = [t for t in trade_logger.trades if t.trade_status == "CLOSED"]
    
    if not closed_trades:
        print("❌ No closed trades available for analysis")
        return
    
    recent_trade = closed_trades[-1]
    base_trade = {
        'strategy': recent_trade.strategy,
        'symbol': recent_trade.symbol,
        'side': recent_trade.side,
        'leverage': recent_trade.leverage,
        'position_size_usdt': recent_trade.position_size_usdt,
        'rsi_entry': recent_trade.rsi_at_entry,
        'actual_pnl': recent_trade.pnl_percentage
    }
    
    print(f"📊 Analyzing scenarios for trade: {recent_trade.trade_id}")
    print(f"🎯 Actual PnL: {recent_trade.pnl_percentage:.2f}%")
    
    scenarios = ml_analyzer.generate_what_if_scenarios(base_trade)
    
    print(f"\n🔍 Generated {len(scenarios)} scenarios:")
    
    # Group by scenario type
    scenario_groups = {}
    for scenario in scenarios:
        scenario_type = scenario['scenario_type']
        if scenario_type not in scenario_groups:
            scenario_groups[scenario_type] = []
        scenario_groups[scenario_type].append(scenario)
    
    for scenario_type, group in scenario_groups.items():
        print(f"\n📋 {scenario_type.upper()} SCENARIOS:")
        
        for scenario in group[:3]:  # Show top 3 scenarios
            prediction = ml_analyzer.predict_trade_outcome(scenario)
            if 'predicted_pnl_percentage' in prediction:
                improvement = prediction['predicted_pnl_percentage'] - base_trade['actual_pnl']
                print(f"  🔄 {scenario}: Predicted PnL: {prediction['predicted_pnl_percentage']:.2f}% (improvement: {improvement:+.2f}%)")

def generate_enhanced_insights():
    """Generate enhanced insights with advanced analytics"""
    print("📊 Generating enhanced insights...")
    
    insights = ml_analyzer.get_enhanced_insights()
    
    if "error" in insights:
        print(f"❌ Error: {insights['error']}")
        return
    
    print("✅ Enhanced insights generated!")
    
    # Show parameter optimization results
    if 'optimization_scenarios' in insights:
        print("\n🎯 PARAMETER OPTIMIZATION RESULTS:")
        for scenario_type, data in insights['optimization_scenarios'].items():
            print(f"  📊 {scenario_type}: {data['avg_improvement']:+.2f}% avg improvement")
    
    # Show market regime analysis  
    if 'market_regime_analysis' in insights:
        print("\n🌊 MARKET REGIME ANALYSIS:")
        regimes = insights['market_regime_analysis']
        for regime, stats in regimes.items():
            print(f"  📈 {regime}: {stats['win_rate']:.1%} win rate ({stats['trade_count']} trades)")
    
    # Show traditional insights
    if 'strategy_performance' in insights:
        print("\n🏆 STRATEGY PERFORMANCE:")
        for strategy, stats in insights['strategy_performance'].items():
            print(f"  📊 {strategy}: {stats['win_rate']:.1f}% win rate, {stats['avg_pnl']:+.2f}% avg PnL")

def main():
    """Enhanced main menu for ML commands"""
    print("🤖 ENHANCED TRADING BOT ML ANALYTICS")
    print("=" * 50)

    while True:
        print("\n🎯 CORE ML FUNCTIONS:")
        print("1. Train ML models")
        print("2. Generate basic insights") 
        print("3. Test prediction")
        
        print("\n🚀 ADVANCED ANALYTICS:")
        print("4. Generate enhanced insights")
        print("5. Run parameter optimization")
        print("6. Analyze what-if scenarios")
        print("7. Get external AI insights")
        
        print("\n📊 REPORTING & DATA:")
        print("8. Send manual daily report")
        print("9. Export trade data")
        print("10. Exit")

        choice = input("\nSelect option (1-10): ")

        if choice == "1":
            train_ml_models()
        elif choice == "2":
            generate_insights()
        elif choice == "3":
            test_prediction()
        elif choice == "4":
            generate_enhanced_insights()
        elif choice == "5":
            run_parameter_optimization()
        elif choice == "6":
            analyze_what_if_scenarios()
        elif choice == "7":
            get_ai_insights()
        elif choice == "8":
            send_manual_report()
        elif choice == "9":
            export_data()
        elif choice == "10":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
