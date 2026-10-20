import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def generate_diagrams():
    os.makedirs("figures", exist_ok=True)
    
    # -------------------------------------------------------------
    # Figure 1: NoSQL Paradigms Taxonomy
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')
    
    # Draw 4 cards for NoSQL types
    cards = [
        {"title": "Document Stores", "examples": "MongoDB, Couchbase", "data_model": "JSON / BSON Trees", "color": "#1E40AF", "accent": "#DBEAFE", "x": 0.05, "y": 0.52, "desc": "Hierarchical, flexible schemas\nNested objects & arrays\nRich indexing capabilities"},
        {"title": "Key-Value Stores", "examples": "Redis, DynamoDB", "data_model": "Key -> Arbitrary Blob", "color": "#065F46", "accent": "#D1FAE5", "x": 0.52, "y": 0.52, "desc": "O(1) dictionary lookups\nExtreme write/read throughput\nMinimal query expression"},
        {"title": "Wide-Column Stores", "examples": "Cassandra, HBase", "data_model": "Sparse Tabular / Column Families", "color": "#9A3412", "accent": "#FFEDD5", "x": 0.05, "y": 0.05, "desc": "Partition key + Clustering cols\nPetabyte distributed scale\nRigid query-bound schemas"},
        {"title": "Graph Databases", "examples": "Neo4j, Amazon Neptune", "data_model": "Property Graph (Nodes/Edges)", "color": "#5B21B6", "accent": "#EDE9FE", "x": 0.52, "y": 0.05, "desc": "Index-free adjacency\nFast relationship traversals\nComplex graph patterns"}
    ]
    
    for c in cards:
        # Card background
        rect = patches.FancyBboxPatch((c["x"], c["y"]), 0.43, 0.42,
                                     boxstyle="round,pad=0.02,rounding_size=0.03",
                                     linewidth=1.5, edgecolor=c["color"], facecolor="white")
        ax.add_patch(rect)
        
        # Header banner
        hdr = patches.FancyBboxPatch((c["x"], c["y"] + 0.31), 0.43, 0.11,
                                    boxstyle="round,pad=0.02,rounding_size=0.02",
                                    linewidth=0, facecolor=c["accent"])
        ax.add_patch(hdr)
        
        ax.text(c["x"] + 0.02, c["y"] + 0.38, c["title"], fontsize=12, fontweight='bold', color=c["color"])
        ax.text(c["x"] + 0.02, c["y"] + 0.33, f"Systems: {c['examples']}", fontsize=9, fontstyle='italic', color='#475569')
        ax.text(c["x"] + 0.02, c["y"] + 0.25, f"Data Model: {c['data_model']}", fontsize=9.5, fontweight='semibold', color='#1E293B')
        ax.text(c["x"] + 0.02, c["y"] + 0.12, c["desc"], fontsize=9, color='#334155', linespacing=1.4)

    plt.suptitle("Figure 1: Taxonomy and Core Paradigms of Contemporary NoSQL DBMS", 
                 fontsize=13, fontweight='bold', color='#0F172A', y=0.98)
    plt.tight_layout()
    plt.savefig("figures/fig1_nosql_taxonomy.png", dpi=300, bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # Figure 2: Cognitive Data Mesh Architecture
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')
    
    # Layer 1: Access / Interface
    r1 = patches.FancyBboxPatch((0.08, 0.78), 0.84, 0.16, boxstyle="round,pad=0.02,rounding_size=0.02",
                                linewidth=1.8, edgecolor='#2563EB', facecolor='#EFF6FF')
    ax.add_patch(r1)
    ax.text(0.5, 0.89, "LAYER 1: UNIFIED POLYGLOT QUERY & NLQ INTERFACE", ha='center', fontsize=11, fontweight='bold', color='#1E40AF')
    ax.text(0.5, 0.82, "Natural Language Processing (NLQ)  •  Unified Declarative Syntax  •  Cross-Model Graph/Vector Query Execution", 
            ha='center', fontsize=9.5, color='#3B82F6')
    
    # Arrow down
    ax.annotate('', xy=(0.5, 0.73), xytext=(0.5, 0.78),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", lw=2, color='#64748B'))
    
    # Layer 2: Universal Semantic Indexing
    r2 = patches.FancyBboxPatch((0.08, 0.48), 0.84, 0.22, boxstyle="round,pad=0.02,rounding_size=0.02",
                                linewidth=1.8, edgecolor='#0D9488', facecolor='#F0FDFA')
    ax.add_patch(r2)
    ax.text(0.5, 0.64, "LAYER 2: UNIVERSAL SEMANTIC INDEXING & EMBEDDING FABRIC", ha='center', fontsize=11, fontweight='bold', color='#0F766E')
    
    # Sub-blocks inside Layer 2
    sub1 = patches.FancyBboxPatch((0.11, 0.51), 0.24, 0.09, boxstyle="round,pad=0.01", facecolor='#CCFBF1', edgecolor='#14B8A6')
    ax.add_patch(sub1)
    ax.text(0.23, 0.55, "Deep Semantic Embeddings\n& Continuous Vectorizer", ha='center', va='center', fontsize=8, fontweight='bold', color='#115E59')
    
    sub2 = patches.FancyBboxPatch((0.38, 0.51), 0.24, 0.09, boxstyle="round,pad=0.01", facecolor='#CCFBF1', edgecolor='#14B8A6')
    ax.add_patch(sub2)
    ax.text(0.50, 0.55, "Global Knowledge Graph\n& Schema Linker", ha='center', va='center', fontsize=8, fontweight='bold', color='#115E59')

    sub3 = patches.FancyBboxPatch((0.65, 0.51), 0.24, 0.09, boxstyle="round,pad=0.01", facecolor='#CCFBF1', edgecolor='#14B8A6')
    ax.add_patch(sub3)
    ax.text(0.77, 0.55, "Adaptive Sharding &\nPredictive Data Routing", ha='center', va='center', fontsize=8, fontweight='bold', color='#115E59')

    # Arrow down
    ax.annotate('', xy=(0.5, 0.43), xytext=(0.5, 0.48),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", lw=2, color='#64748B'))

    # Layer 3: Heterogeneous Storage Engines
    r3 = patches.FancyBboxPatch((0.08, 0.12), 0.84, 0.28, boxstyle="round,pad=0.02,rounding_size=0.02",
                                linewidth=1.8, edgecolor='#475569', facecolor='#F1F5F9')
    ax.add_patch(r3)
    ax.text(0.5, 0.34, "LAYER 3: ADAPTIVE MULTI-ENGINE STORAGE FABRIC", ha='center', fontsize=11, fontweight='bold', color='#1E293B')
    
    # 4 engines inside Layer 3
    engs = [
        {"name": "Document Node\n(BSON/JSON)", "x": 0.11},
        {"name": "Key-Value Node\n(In-Memory Hash)", "x": 0.30},
        {"name": "Wide-Column Node\n(SSTable / LSM)", "x": 0.49},
        {"name": "Graph Node\n(Adjacency Index)", "x": 0.68}
    ]
    for e in engs:
        box = patches.FancyBboxPatch((e["x"], 0.15), 0.17, 0.15, boxstyle="round,pad=0.01", facecolor='white', edgecolor='#94A3B8', lw=1.2)
        ax.add_patch(box)
        ax.text(e["x"] + 0.085, 0.22, e["name"], ha='center', va='center', fontsize=8.5, fontweight='semibold', color='#334155')

    plt.suptitle("Figure 2: The Cognitive Data Mesh Architectural Framework", 
                 fontsize=13, fontweight='bold', color='#0F172A', y=0.98)
    plt.tight_layout()
    plt.savefig("figures/fig2_cognitive_data_mesh.png", dpi=300, bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # Figure 3: CAP Trade-offs & Complexity Spectrum
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    
    # Left: Triangle
    ax1.set_facecolor('#F8FAFC')
    ax1.axis('off')
    tri = patches.Polygon([[0.5, 0.85], [0.12, 0.18], [0.88, 0.18]], closed=True, 
                          facecolor='#E2E8F0', edgecolor='#334155', lw=2)
    ax1.add_patch(tri)
    
    ax1.text(0.5, 0.90, "Consistency (C)", ha='center', fontsize=11, fontweight='bold', color='#1E3A8A')
    ax1.text(0.06, 0.12, "Availability (A)", ha='center', fontsize=11, fontweight='bold', color='#065F46')
    ax1.text(0.94, 0.12, "Partition Tolerance (P)", ha='center', fontsize=11, fontweight='bold', color='#9A3412')
    
    # Systems in triangle
    ax1.text(0.30, 0.55, "CA\nRDBMS", ha='center', fontsize=9, fontweight='bold', color='#1E293B')
    ax1.text(0.70, 0.55, "CP\nMongoDB, HBase", ha='center', fontsize=9, fontweight='bold', color='#1E293B')
    ax1.text(0.50, 0.23, "AP\nCassandra, DynamoDB", ha='center', fontsize=9, fontweight='bold', color='#1E293B')
    
    # Cognitive Mesh Overlay
    cog_circle = patches.Circle((0.5, 0.48), 0.14, facecolor='#FEF08A', edgecolor='#CA8A04', lw=2, linestyle='--')
    ax1.add_patch(cog_circle)
    ax1.text(0.5, 0.48, "Cognitive Data Mesh\n(Dynamic Tunable PACELC)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#854D0E')
    ax1.set_title("(a) CAP Theorem & Tunable Consistency", fontsize=11, fontweight='bold', color='#1E293B')

    # Right: Complexity vs Semantic Awareness
    ax2.set_facecolor('#FFFFFF')
    models = ['Key-Value', 'Wide-Column', 'Document', 'Graph', 'Cognitive Mesh']
    schema_flex = [2, 4, 8, 9, 10]
    semantic_int = [1, 2, 3, 5, 9.5]
    
    bar_width = 0.35
    import numpy as np
    x = np.arange(len(models))
    
    rects1 = ax2.bar(x - bar_width/2, schema_flex, bar_width, label='Schema Flexibility', color='#3B82F6')
    rects2 = ax2.bar(x + bar_width/2, semantic_int, bar_width, label='Semantic Intelligence', color='#10B981')
    
    ax2.set_ylabel('Capability Index (1 - 10)', fontsize=10, fontweight='semibold', color='#334155')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, rotation=25, ha='right', fontsize=9, fontweight='medium')
    ax2.set_ylim(0, 11)
    ax2.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=8.5)
    ax2.grid(axis='y', linestyle=':', alpha=0.6)
    ax2.set_title("(b) Schema Flexibility vs. Semantic Intelligence", fontsize=11, fontweight='bold', color='#1E293B')

    plt.suptitle("Figure 3: Distributed System Trade-Offs and Architectural Evolution", 
                 fontsize=12.5, fontweight='bold', color='#0F172A', y=0.98)
    plt.tight_layout()
    plt.savefig("figures/fig3_cap_tradeoffs.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Figures generated successfully.")

if __name__ == "__main__":
    generate_diagrams()
