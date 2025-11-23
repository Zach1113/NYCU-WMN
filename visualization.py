"""
Visualization module for QoS simulation results.
"""

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def plot_comparison(results, metric='avg_latency', title=None, save_path=None):
    """
    Create a bar chart comparing a specific metric across strategies.
    
    Args:
        results: Dictionary mapping strategy name to metrics
        metric: Metric to plot
        title: Plot title
        save_path: Path to save figure (optional)
    """
    strategies = list(results.keys())
    values = [results[s][metric] for s in strategies]
    
    # Generate colors dynamically based on number of strategies
    colors = cm.get_cmap('tab10')(np.linspace(0, 0.3, len(strategies)))
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(strategies, values, color=colors)
    plt.xlabel('Queuing Strategy', fontsize=12)
    plt.ylabel(metric.replace('_', ' ').title(), fontsize=12)
    
    if title:
        plt.title(title, fontsize=14, fontweight='bold')
    else:
        plt.title(f'{metric.replace("_", " ").title()} Comparison', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")
    
    return plt.gcf()


def plot_all_metrics(results, save_path=None):
    """
    Create a comprehensive comparison of all metrics including both fairness types.
    
    Args:
        results: Dictionary mapping strategy name to metrics
        save_path: Path to save figure (optional)
    """
    strategies = list(results.keys())
    metrics = ['avg_latency', 'avg_waiting_time', 'throughput', 
               'fairness_index', 'flow_fairness_index']
    metric_labels = ['Avg Latency', 'Avg Waiting Time', 'Throughput', 
                     'Per-Packet Fairness', 'Per-Flow Fairness']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('QoS Queuing Strategies - Performance Comparison', 
                 fontsize=16, fontweight='bold')
    
    axes = axes.flatten()
    # Generate colors dynamically based on number of strategies
    colors = cm.get_cmap('tab10')(np.linspace(0, 0.3, len(strategies)))
    
    for idx, (metric, label) in enumerate(zip(metrics, metric_labels)):
        values = [results[s][metric] for s in strategies]
        bars = axes[idx].bar(strategies, values, color=colors)
        axes[idx].set_xlabel('Strategy', fontsize=11)
        axes[idx].set_ylabel(label, fontsize=11)
        axes[idx].set_title(label, fontsize=12, fontweight='bold')
        axes[idx].grid(axis='y', alpha=0.3)
        
        # Rotate x-axis labels if needed
        axes[idx].tick_params(axis='x', rotation=15)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            axes[idx].text(bar.get_x() + bar.get_width()/2., height,
                          f'{height:.3f}',
                          ha='center', va='bottom', fontsize=9)
    
    # Hide the 6th subplot (we only have 5 metrics)
    axes[5].axis('off')
    
    # Add explanation text in the empty subplot
    explanation = (
        "Fairness Metrics Explained:\n\n"
        "Per-Packet Fairness:\n"
        "  • Measures variance in individual packet latencies\n"
        "  • Higher = all packets treated similarly\n"
        "  • FCFS typically scores highest\n\n"
        "Per-Flow Fairness:\n"
        "  • Measures variance in average latency per flow\n"
        "  • Higher = flows get equal service\n"
        "  • Fair Queue optimizes for this metric"
    )
    axes[5].text(0.1, 0.5, explanation, fontsize=10, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved comprehensive plot to {save_path}")
    
    return fig



def plot_latency_distribution(strategies_packets, save_path=None):
    """
    Plot latency distribution for each strategy.
    
    Args:
        strategies_packets: Dict mapping strategy name to list of processed packets
        save_path: Path to save figure (optional)
    """
    fig, axes = plt.subplots(1, len(strategies_packets), figsize=(15, 5))
    
    if len(strategies_packets) == 1:
        axes = [axes]
    
    fig.suptitle('Latency Distribution by Strategy', fontsize=14, fontweight='bold')
    
    for idx, (strategy_name, packets) in enumerate(strategies_packets.items()):
        latencies = [p.get_latency() for p in packets if p.get_latency() is not None]
        
        if not latencies:
            # Skip if no latency data
            axes[idx].text(0.5, 0.5, 'No data', ha='center', va='center')
            axes[idx].set_title(strategy_name, fontsize=11, fontweight='bold')
            continue
        
        axes[idx].hist(latencies, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        axes[idx].set_xlabel('Latency (s)', fontsize=10)
        axes[idx].set_ylabel('Frequency', fontsize=10)
        axes[idx].set_title(strategy_name, fontsize=11, fontweight='bold')
        axes[idx].grid(axis='y', alpha=0.3)
        
        # Add mean line
        mean_lat = np.mean(latencies)
        axes[idx].axvline(mean_lat, color='red', linestyle='--', linewidth=2, 
                         label=f'Mean: {mean_lat:.2f}')
        axes[idx].legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved latency distribution plot to {save_path}")
    
    return fig


def plot_priority_fairness(packets_by_priority, strategy_name, save_path=None):
    """
    Plot average latency by priority level to assess fairness.
    
    Args:
        packets_by_priority: Dict mapping priority level to list of packets
        strategy_name: Name of the strategy
        save_path: Path to save figure (optional)
    """
    priorities = sorted(packets_by_priority.keys())
    avg_latencies = []
    
    for priority in priorities:
        packets = packets_by_priority[priority]
        latencies = [p.get_latency() for p in packets if p.get_latency() is not None]
        avg_latencies.append(np.mean(latencies) if latencies else 0)
    
    plt.figure(figsize=(10, 6))
    # Generate colors dynamically
    colors = cm.get_cmap('viridis')(np.linspace(0.2, 0.8, len(priorities)))
    bars = plt.bar([f'Priority {p}' for p in priorities], avg_latencies, color=colors)
    plt.xlabel('Priority Level', fontsize=12)
    plt.ylabel('Average Latency (s)', fontsize=12)
    plt.title(f'{strategy_name} - Fairness Analysis\n(Average Latency by Priority)', 
             fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved fairness plot to {save_path}")
    
    return plt.gcf()


def print_results_table(results):
    """
    Print a formatted table of results with both fairness metrics.
    
    Args:
        results: Dictionary mapping strategy name to metrics
    """
    print("\n" + "="*100)
    print("PERFORMANCE METRICS COMPARISON")
    print("="*100)
    print(f"{'Strategy':<20} {'Avg Latency':<15} {'Avg Waiting':<15} {'Throughput':<15} "
          f"{'Pkt Fair':<12} {'Flow Fair':<12}")
    print("-"*100)
    
    for strategy, metrics in results.items():
        print(f"{strategy:<20} {metrics['avg_latency']:<15.4f} "
              f"{metrics['avg_waiting_time']:<15.4f} {metrics['throughput']:<15.4f} "
              f"{metrics['fairness_index']:<12.4f} {metrics['flow_fairness_index']:<12.4f}")
    
    print("="*100)
    print("Note: 'Pkt Fair' = Per-Packet Fairness, 'Flow Fair' = Per-Flow Fairness")
    print("      Higher values indicate better fairness (range: 0-1)")
    print("="*100 + "\n")

