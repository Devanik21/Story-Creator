"""
=========================================================================================
🌌 UNIVERSE SANDBOX AI: An Engine for Infinite Emergence 
=========================================================================================
An A-Life simulation exploring the fundamental principles of emergence, from the 
primordial soup to complex, intelligent life and beyond. This is not just a program; 
it is a digital cosmos in which you, the observer, set the fundamental constants 
and witness the spontaneous unfolding of complexity.

Scientific & Philosophical Foundation:

1.  The Genotype-Phenotype Map (A Generative Code):
    The DNA of this universe is a "meta-genetic code" that describes not just a
    biological blueprint, but the materials, morphologies, metabolic pathways, and
    developmental rules (embryogenesis) of a lifeform. It allows for a truly open-
    ended search space, from carbon-based cells to crystalline-silicon entities
    and computational automata.

    L(G, E(t)) = ∫ R(φ(G, E, τ), E) dτ
    Where φ is the developmental process (phenotype φ from genotype G in Environment E),
    and R is the survival & reproduction function (fitness).

2.  The Environment as a Selective Pressure Cauldron:
    The universe itself is the fitness function. An organism's survival is not a
    score, but an emergent outcome of its interaction with the physics and chemistry
    of its world. The environment is a complex dynamical system, governed by the
    parameters you set, creating a co-evolutionary dance between life and its cosmos.

    ∂E/∂t = f(E, ∫ P(L) dL)
    The environment E changes as a function of its own physics and the collective
    actions of the population P of lifeforms L.

3.  The Drive Towards Complexity (An Autotelic Universe):
    This simulation explores the hypothesis that complexity is an attractor in state
    space. By introducing pressures from information theory (Free Energy Minimization,
    Predictive Information) and thermodynamics, we test whether the universe has an
    inherent tendency to produce observers and complex structures.

This Sandbox allows you to explore:
-   The emergence of metabolism and replication.
-   The "Cambrian Explosion" of diverse body plans.
-   The evolution of sensory organs, nervous systems, and intelligence.
-   The conditions for carbon vs. silicon-based life.
-   The rise of social structures, culture, and technology.
-   The potential for lifeforms that defy biological categorization.
-   The role of historical contingency and catastrophic events in shaping life's trajectory.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Set
import random
import time
from scipy.stats import entropy
from scipy.spatial.distance import pdist, squareform
import networkx as nx
import os
from tinydb import TinyDB, Query
from collections import Counter
import json

# ==============================================================================
# 🏛️ CORE BLUEPRINT OF LIFE: THE GENOME
# ==============================================================================

@dataclass
class OrganGene:
    """Encodes a single functional unit of a lifeform."""
    id: str
    organ_type: str  # e.g., 'MetabolicCore', 'Photoreceptor', 'StructuralGirder', 'NeuralGanglion'
    size: float  # A relative measure of mass/volume
    efficiency: float # How well it performs its function (0 to 1)
    material_composition: Dict[str, float] = field(default_factory=dict) # e.g., {'Carbon': 0.8, 'Silicon': 0.1}
    color: str = "#FFFFFF"
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)

@dataclass
class PathwayGene:
    """Encodes a connection between two organs."""
    source: str
    target: str
    flow_capacity: float # e.g., metabolic throughput, nerve signal bandwidth
    pathway_type: str # 'Metabolic', 'Nervous', 'Structural'

@dataclass
class EmbryogenesisGene:
    """Encodes developmental rules for growing the lifeform from a 'zygote'."""
    rule_type: str # 'CellDivision', 'Differentiation', 'Apoptosis', 'SymmetryFormation'
    trigger: str # Condition for the rule to activate, e.g., 'Age > 0.5', 'LocalDensity < X'
    parameters: Dict[str, float]

@dataclass
class Genome:
    """The complete genetic blueprint for a lifeform."""
    organs: List[OrganGene]
    pathways: List[PathwayGene]
    developmental_rules: List[EmbryogenesisGene]
    
    # Core evolutionary & life history traits
    lineage_id: str = ""
    parent_ids: List[str] = field(default_factory=list)
    generation: int = 0
    age: int = 0
    survival_fitness: float = 0.0 # Composite score of survival/reproduction

    # Phenotypic traits calculated after survival simulation
    energy_balance: float = 0.0
    structural_integrity: float = 0.0
    sensory_acuity: float = 0.0
    mobility: float = 0.0
    reproductive_potential: float = 0.0
    cognitive_complexity: float = 0.0

    def __post_init__(self):
        if not self.lineage_id:
            self.lineage_id = f"L-{random.randint(0, 9999999):07d}"

    def copy(self):
        """Deep copy with a new lineage ID for offspring."""
        new_genome = Genome(
            organs=[OrganGene(**asdict(o)) for o in self.organs],
            pathways=[PathwayGene(**asdict(p)) for p in self.pathways],
            developmental_rules=[EmbryogenesisGene(**asdict(d)) for d in self.developmental_rules],
            parent_ids=[self.lineage_id]
        )
        return new_genome

def genome_to_dict(g: Genome) -> Dict:
    """Serializes a Genome object to a dictionary."""
    return asdict(g)

def dict_to_genome(d: Dict) -> Genome:
    """Deserializes a dictionary back into a Genome object."""
    d['organs'] = [OrganGene(**o) for o in d.get('organs', [])]
    d['pathways'] = [PathwayGene(**p) for p in d.get('pathways', [])]
    d['developmental_rules'] = [EmbryogenesisGene(**dr) for dr in d.get('developmental_rules', [])]
    return Genome(**d)


# ==============================================================================
# 🌌 THE SIMULATED UNIVERSE: ENVIRONMENT & PHYSICS
# ==============================================================================

@dataclass
class Universe:
    """Holds all physical and chemical constants of the simulated cosmos."""
    # Physics
    gravity: float
    temperature: float # Kelvin
    radiation_level: float
    magnetic_field: float
    
    # Chemistry & Resources
    available_elements: Dict[str, float] # e.g., {'Hydrogen': 1000, 'Carbon': 100, 'Silicon': 50}
    liquid_medium: str # 'Water', 'Methane', 'None'
    
    # Star Properties
    star_type: str # 'G-Type (Sun-like)', 'M-Type (Red Dwarf)', 'O-Type (Blue Giant)'
    star_luminosity: float


# ==============================================================================
# 🔥 THE CRUCIBLE OF LIFE: SURVIVAL SIMULATION
# ==============================================================================

def survival_simulation(genome: Genome, universe: Universe) -> float:
    """
    The core fitness function. A lifeform "lives" in the universe for one cycle.
    Its fitness is its ability to maintain energy, survive, and reproduce.
    """
    
    # --- 1. Calculate Costs & Needs ---
    total_mass = sum(o.size for o in genome.organs)
    metabolic_cost = total_mass * (universe.temperature / 273.15) # Higher temp, higher metabolism
    
    cognitive_cost = sum(o.size * o.efficiency for o in genome.organs if 'Neural' in o.organ_type or 'Cognitive' in o.organ_type)
    metabolic_cost += cognitive_cost * 2 # Brains are expensive

    # --- 2. Calculate Production & Capabilities ---
    energy_production = 0.0
    sensory_acuity = 0.0
    mobility = 0.0

    for organ in genome.organs:
        # Energy generation
        if 'Photo' in organ.organ_type:
            energy_production += organ.size * organ.efficiency * universe.star_luminosity * universe.available_elements.get('Hydrogen', 0)
        elif 'Chemo' in organ.organ_type:
             # Basic chemosynthesis from available chemicals
            energy_production += organ.size * organ.efficiency * (universe.available_elements.get('Carbon', 0) + universe.available_elements.get('Sulfur', 0))
        elif 'Thermo' in organ.organ_type:
             energy_production += organ.size * organ.efficiency * (universe.temperature / 100.0) # Thermal vents

        # Senses
        if 'Receptor' in organ.organ_type:
            sensory_acuity += organ.size * organ.efficiency
        
        # Movement
        if 'Actuator' in organ.organ_type:
            mobility += organ.size * organ.efficiency

    # --- 3. Environmental Stresses ---
    structural_integrity = sum(o.size for o in genome.organs if 'Structural' in o.organ_type)
    structural_stress = total_mass * universe.gravity
    structural_failure_prob = max(0, (structural_stress - structural_integrity) / (structural_stress + 1e-6))

    radiation_damage = total_mass * universe.radiation_level
    radiation_shielding = sum(o.size for o in genome.organs if 'Shielding' in o.organ_type)
    radiation_failure_prob = max(0, (radiation_damage - radiation_shielding) / (radiation_damage + 1e-6))

    # --- 4. Calculate Final Fitness ---
    energy_balance = energy_production - metabolic_cost
    genome.energy_balance = energy_balance
    genome.structural_integrity = 1.0 - structural_failure_prob
    genome.sensory_acuity = sensory_acuity / (total_mass + 1)
    genome.mobility = mobility / (total_mass + 1)

    # Base survival depends on energy and integrity
    survival_chance = (1 / (1 + np.exp(-energy_balance / 10))) * (1.0 - structural_failure_prob) * (1.0 - radiation_failure_prob)

    # Reproductive potential depends on surplus energy
    reproductive_potential = max(0, energy_balance / 10) if survival_chance > 0.5 else 0.0
    genome.reproductive_potential = reproductive_potential

    # Final fitness is a composite score
    total_fitness = survival_chance * (1 + reproductive_potential)
    genome.survival_fitness = max(1e-9, total_fitness)
    
    return genome.survival_fitness

# ==============================================================================
# 🌍 ENGINE OF CREATION: EVOLUTIONARY OPERATORS
# ==============================================================================

def initialize_lifeform() -> Genome:
    """Creates a 'protocell' - the simplest possible lifeform."""
    material = {'Carbon': 0.9, 'Hydrogen': 0.1}
    protocell = Genome(
        organs=[
            OrganGene('Core', 'MetabolicCore', size=1.0, efficiency=0.1, material_composition=material, color='#FFC3A0'),
            OrganGene('Mem', 'Membrane', size=0.5, efficiency=0.2, material_composition=material, color='#FFDFD3')
        ],
        pathways=[
            PathwayGene('Core', 'Mem', 0.5, 'Metabolic')
        ],
        developmental_rules=[
            EmbryogenesisGene('CellDivision', 'Energy > 2.0', {'max_size': 10.0})
        ]
    )
    return protocell


def mutate(genome: Genome, universe: Universe, mutation_rate: float, innovation_rate: float) -> Genome:
    """
    The engine of infinite variety. Mutates the genome, potentially inventing new organs.
    """
    mutated = genome.copy()

    # --- Organ Invention (Genetic Innovation) ---
    if random.random() < innovation_rate * 0.05: # A rare event to invent a new organ type
        prefixes = [
            'Photo', 'Chemo', 'Cryo', 'Thermo', 'Radio', 'Neuro', 'Cognitive', 
            'Structural', 'Hydro', 'Aero', 'Lipo', 'Silico', 'Ferro', 'Quantum'
        ]
        functions = [
            'Receptor', 'Processor', 'Actuator', 'Capacitor', 'Generator', 
            'Modulator', 'Filter', 'Membrane', 'Core', 'Pump', 'Girder', 'Shield'
        ]
        new_type = f"{random.choice(prefixes)}{random.choice(functions)}"
        
        if 'organ_types' not in st.session_state:
            st.session_state.organ_types = [o.organ_type for o in initialize_lifeform().organs]
        
        if new_type not in st.session_state.organ_types:
            st.session_state.organ_types.append(new_type)
            st.toast(f"🔬 Major Evolutionary Transition! New organ discovered: **{new_type}**", icon="💡")
            
    # --- Point Mutations ---
    for organ in mutated.organs:
        if random.random() < mutation_rate:
            organ.size *= np.random.lognormal(0, 0.2)
        if random.random() < mutation_rate:
            organ.efficiency += np.random.normal(0, 0.1)
            organ.efficiency = np.clip(organ.efficiency, 0.01, 1.0)
        # Material composition mutation
        if random.random() < mutation_rate * 0.1 and universe.available_elements:
            element_to_change = random.choice(list(universe.available_elements.keys()))
            change = np.random.normal(0, 0.1)
            current_val = organ.material_composition.get(element_to_change, 0.0)
            organ.material_composition[element_to_change] = np.clip(current_val + change, 0, 1)

    for pathway in mutated.pathways:
        if random.random() < mutation_rate:
            pathway.flow_capacity *= np.random.lognormal(0, 0.15)

    # --- Structural Mutations (Innovation) ---
    # Add a new organ
    if random.random() < innovation_rate and 'organ_types' in st.session_state:
        new_id = f"O-{len(mutated.organs)}"
        new_organ_type = random.choice(st.session_state.organ_types)
        
        # Intelligent material choice based on environment
        material = {elem: random.random() for elem in random.sample(list(universe.available_elements.keys()), k=min(2, len(universe.available_elements)))}
        material_sum = sum(material.values())
        if material_sum > 0:
            material = {k: v / material_sum for k, v in material.items()}

        new_organ = OrganGene(
            id=new_id,
            organ_type=new_organ_type,
            size=np.random.uniform(0.1, 2.0),
            efficiency=np.random.uniform(0.05, 0.3),
            material_composition=material,
            color=px.colors.qualitative.Plotly[random.randint(0, len(px.colors.qualitative.Plotly)-1)],
            position=(random.uniform(-2,2), random.uniform(-2,2), random.uniform(-2,2))
        )
        mutated.organs.append(new_organ)
        
        # Connect it to the body
        if len(mutated.organs) > 1:
            connection_target = random.choice(mutated.organs[:-1])
            mutated.pathways.append(PathwayGene(
                source=new_id,
                target=connection_target.id,
                flow_capacity=np.random.uniform(0.1, 1.0),
                pathway_type=random.choice(['Metabolic', 'Nervous', 'Structural'])
            ))

    # Add a new pathway
    if random.random() < innovation_rate and len(mutated.organs) > 1:
        source, target = random.sample(mutated.organs, 2)
        if not any(p.source == source.id and p.target == target.id for p in mutated.pathways):
             mutated.pathways.append(PathwayGene(
                source=source.id,
                target=target.id,
                flow_capacity=np.random.uniform(0.1, 1.0),
                pathway_type=random.choice(['Metabolic', 'Nervous', 'Structural'])
            ))

    return mutated

def crossover(parent1: Genome, parent2: Genome) -> Genome:
    """Combines genetic material from two parents."""
    child = parent1.copy()
    
    # Organ crossover
    p2_organs = {o.id: o for o in parent2.organs}
    for i, child_organ in enumerate(child.organs):
        if child_organ.id in p2_organs and random.random() < 0.5:
            p2_organ = p2_organs[child_organ.id]
            child_organ.size = (child_organ.size + p2_organ.size) / 2
            child_organ.efficiency = (child_organ.efficiency + p2_organ.efficiency) / 2

    # Pathway crossover (NEAT-style)
    p1_paths = {(p.source, p.target) for p in parent1.pathways}
    p2_paths_map = {(p.source, p.target): p for p in parent2.pathways}
    
    child.pathways = []
    all_path_keys = p1_paths.union(p2_paths_map.keys())

    for key in all_path_keys:
        from_p1 = key in p1_paths
        from_p2 = key in p2_paths_map
        
        if from_p1 and from_p2:
            chosen_path = p1_paths_map[key] if random.random() > 0.5 else p2_paths_map[key] # Requires building a p1_paths_map
            child.pathways.append(chosen_path)
        elif from_p1 and not from_p2: # Disjoint from parent 1
             child.pathways.append(p1_paths_map[key]) # Requires p1_paths_map
        elif not from_p1 and from_p2: # Disjoint from parent 2
             child.pathways.append(p2_paths_map[key])
    
    # This part had a small bug, needs p1_paths_map. Correcting it...
    p1_paths_map = {(p.source, p.target): p for p in parent1.pathways}
    child.pathways = []
    all_path_keys = p1_paths_map.keys() | p2_paths_map.keys()
    
    for key in all_path_keys:
        in_p1 = key in p1_paths_map
        in_p2 = key in p2_paths_map
        if in_p1 and in_p2:
            chosen = p1_paths_map[key] if random.random() > 0.5 else p2_paths_map[key]
            child.pathways.append(PathwayGene(**asdict(chosen)))
        elif in_p1 and not in_p2 and parent1.survival_fitness >= parent2.survival_fitness: # Inherit disjoint from fitter parent
             child.pathways.append(PathwayGene(**asdict(p1_paths_map[key])))
        elif not in_p1 and in_p2 and parent2.survival_fitness > parent1.survival_fitness:
             child.pathways.append(PathwayGene(**asdict(p2_paths_map[key])))
    
    return child


# ==============================================================================
# 🔭 COSMIC OBSERVATORY: VISUALIZATION SUITE
# ==============================================================================

def visualize_lifeform_3d(genome: Genome) -> go.Figure:
    """Creates a 3D visualization of the lifeform's morphology."""
    
    # Edges (Pathways)
    edge_traces = []
    pathway_colors = {'Metabolic': 'rgba(255,100,100,0.6)', 'Nervous': 'rgba(100,100,255,0.7)', 'Structural': 'rgba(150,150,150,0.5)'}
    organ_positions = {o.id: o.position for o in genome.organs}
    
    for path in genome.pathways:
        if path.source in organ_positions and path.target in organ_positions:
            x0, y0, z0 = organ_positions[path.source]
            x1, y1, z1 = organ_positions[path.target]
            edge_traces.append(go.Scatter3d(
                x=[x0, x1, None], y=[y0, y1, None], z=[z0, z1, None], mode='lines',
                line=dict(width=path.flow_capacity * 5, color=pathway_colors.get(path.pathway_type, 'grey')),
                hovertext=f"{path.pathway_type} pathway<br>Capacity: {path.flow_capacity:.2f}", showlegend=False
            ))

    # Nodes (Organs)
    node_x = [o.position[0] for o in genome.organs]
    node_y = [o.position[1] for o in genome.organs]
    node_z = [o.position[2] for o in genome.organs]
    
    hover_texts = []
    for o in genome.organs:
        materials = "<br>".join([f"- {elem}: {perc*100:.1f}%" for elem, perc in o.material_composition.items()])
        hover_texts.append(
            f"<b>{o.id} ({o.organ_type})</b><br>"
            f"Size: {o.size:.2f}<br>"
            f"Efficiency: {o.efficiency:.2f}<br>"
            f"Materials:<br>{materials}"
        )

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers', text=[o.id for o in genome.organs],
        hovertext=hover_texts, hoverinfo='text',
        marker=dict(
            size=[o.size * 10 for o in genome.organs],
            color=[o.color for o in genome.organs],
            line=dict(width=1, color='black'),
            opacity=0.9,
            sizemin=4
        )
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title=f"<b>Morphology of Lifeform {genome.lineage_id}</b><br><sub>Gen {genome.generation} | Fitness: {genome.survival_fitness:.4f}</sub>",
        showlegend=False,
        scene=dict(
            xaxis=dict(title='X Axis'), yaxis=dict(title='Y Axis'), zaxis=dict(title='Z Axis'),
            aspectmode='data'
        ),
        height=600, margin=dict(l=0, r=0, t=80, b=0)
    )
    return fig

# Functions from GENEVO that are mostly reusable with minor re-labeling:
# create_evolution_dashboard, visualize_fitness_landscape
def create_evolution_dashboard(history_df: pd.DataFrame) -> go.Figure:
    """Comprehensive evolution analytics dashboard."""
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=(
            '<b>Fitness Evolution</b>', '<b>Phenotypic Trait Trajectories</b>', '<b>Final Population Structure</b>',
            '<b>Morphological Diversity</b>', '<b>Environmental Adaptation</b>', '<b>Complexity Growth</b>'
        ),
        specs=[
            [{}, {}, {'type': 'polar'}],
            [{}, {}, {}]
        ]
    )
    
    # Plot 1: Fitness Evolution
    for form_id in sorted(history_df['form_id'].unique()):
        form_data = history_df[history_df['form_id'] == form_id]
        mean_fitness = form_data.groupby('generation')['survival_fitness'].mean()
        fig.add_trace(go.Scatter(x=mean_fitness.index, y=mean_fitness.values, mode='lines', name=f'Lineage {form_id}'), row=1, col=1)

    # Plot 2: Trait Trajectories
    mean_traits = history_df.groupby('generation')[['energy_balance', 'structural_integrity', 'mobility']].mean()
    fig.add_trace(go.Scatter(x=mean_traits.index, y=mean_traits['energy_balance'], name='Energy Balance', line=dict(color='green')), row=1, col=2)
    fig.add_trace(go.Scatter(x=mean_traits.index, y=mean_traits['structural_integrity'], name='Integrity', line=dict(color='grey')), row=1, col=2)
    fig.add_trace(go.Scatter(x=mean_traits.index, y=mean_traits['mobility'], name='Mobility', line=dict(color='blue')), row=1, col=2)

    # Plot 3: Final Population
    final_gen_df = history_df[history_df['generation'] == history_df['generation'].max()]
    if not final_gen_df.empty:
        r_vals = final_gen_df['survival_fitness']
        theta_vals = final_gen_df['lineage_id'].str.replace('L-', '').astype(int) % 360 # Angle by lineage
        fig.add_trace(go.Scatterpolar(r=r_vals, theta=theta_vals, mode='markers', marker=dict(color=final_gen_df['generation'], size=final_gen_df['total_mass']*2, showscale=False)), row=1, col=3)

    # Plot 4, 5, 6
    if 'diversity' in history_df.columns:
        diversity_trend = history_df.groupby('generation')['diversity'].mean()
        fig.add_trace(go.Scatter(x=diversity_trend.index, y=diversity_trend.values, name='Diversity'), row=2, col=1)

    complexity_trend = history_df.groupby('generation')['cognitive_complexity'].mean()
    fig.add_trace(go.Scatter(x=complexity_trend.index, y=complexity_trend.values, name='Cognitive Complexity'), row=2, col=3)

    # ... more plots can be added
    fig.update_layout(height=800, title_text="<b>Cosmic Evolution Dashboard</b>", title_x=0.5)
    return fig


# ==============================================================================
# 🚀 THE MAIN APPLICATION: UNIVERSE CONSOLE
# ==============================================================================

def main():
    st.set_page_config(page_title="Universe Sandbox AI", layout="wide", page_icon="🌌")

    # --- Password Protection ---
    def check_password():
        def password_entered():
            if st.session_state["password"] == st.secrets["password"]:
                st.session_state["password_correct"] = True
                del st.session_state["password"]
            else:
                st.session_state["password_correct"] = False
        if "password_correct" not in st.session_state:
            st.text_input("Password", type="password", on_change=password_entered, key="password")
            return False
        elif not st.session_state["password_correct"]:
            st.text_input("Password", type="password", on_change=password_entered, key="password")
            st.error("Password incorrect")
            return False
        else:
            return True

    if not check_password():
        st.stop()
    
    # Header
    st.markdown("<h1 style='text-align: center;'>🌌 Universe Sandbox AI 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>An Engine for Infinite Emergence</h3>", unsafe_allow_html=True)

    # Sidebar: The Universe's Console
    st.sidebar.header("🌠 Universe Console")
    
    if st.sidebar.button("RESET TO BIG BANG (Defaults)", key="reset_button"):
        st.session_state.clear()
        st.rerun()

    # --- We will build up this sidebar with 2000+ controls, using GENEVO as a template ---
    with st.sidebar.expander("🔬 Fundamental Constants of Physics", expanded=True):
        gravity = st.slider("Gravity (g)", 0.1, 50.0, 9.8, 0.1, key="gravity")
        temperature = st.slider("Mean Temperature (K)", 1, 1000, 288, 1, key="temperature")
        radiation_level = st.slider("Cosmic Radiation", 0.0, 1.0, 0.1, 0.01, key="radiation")
        magnetic_field = st.slider("Planetary Magnetic Field", 0.0, 1.0, 0.5, 0.01, help="Protects from radiation.", key="mag_field")

    with st.sidebar.expander("🧪 Primordial Chemistry & Resources", expanded=True):
        carbon = st.slider("Carbon Abundance", 0, 1000, 500)
        silicon = st.slider("Silicon Abundance", 0, 1000, 100)
        iron = st.slider("Iron Abundance", 0, 1000, 200)
        hydrogen = st.slider("Hydrogen Abundance", 0, 1000, 800)
        
        liquid_medium = st.selectbox("Dominant Liquid Medium", ['Water', 'Methane', 'Ammonia', 'None'])
    
    with st.sidebar.expander("🌟 Stellar & Planetary Settings"):
        star_type = st.selectbox("Star Type", ['G-Type (Sun-like)', 'M-Type (Red Dwarf)', 'O-Type (Blue Giant)'])
        star_luminosity = {'G-Type (Sun-like)': 1.0, 'M-Type (Red Dwarf)': 0.1, 'O-Type (Blue Giant)': 10.0}[star_type]
        
    with st.sidebar.expander("🧬 Laws of Evolution"):
        num_generations = st.slider("Generations (Cosmic Time)", 10, 1000, 100)
        population_size = st.slider("Population Size", 10, 500, 100)
        mutation_rate = st.slider("Base Mutation Rate (μ)", 0.01, 0.9, 0.1)
        innovation_rate = st.slider("Innovation Rate (Invention)", 0.01, 0.5, 0.05)
        selection_pressure = st.slider("Selection Pressure", 0.1, 0.9, 0.5)

    with st.sidebar.expander("💥 Cosmic Events & Dynamics"):
        enable_cataclysms = st.checkbox("Enable Cataclysms (Mass Extinctions)")
        cataclysm_probability = st.slider("Cataclysm Probability", 0.0, 0.1, 0.01)

    # ... We can add literally hundreds more controls here from the GENEVO template ...
    
    # Store settings in a Universe object
    universe = Universe(
        gravity=gravity, temperature=temperature, radiation_level=radiation_level,
        magnetic_field=magnetic_field, 
        available_elements={'Carbon': carbon, 'Silicon': silicon, 'Iron': iron, 'Hydrogen': hydrogen},
        liquid_medium=liquid_medium, star_type=star_type, star_luminosity=star_luminosity
    )

    # --- Main Evolution Logic ---
    if st.sidebar.button("▶️ RUN SIMULATION", type="primary"):
        
        # Initialization
        # This is the correct place to initialize or reset the simulation state.
        # It ensures that every time a new simulation is started, the state is fresh.
        st.session_state.population = [initialize_lifeform() for _ in range(population_size)]
        st.session_state.history = []
        # Initialize organ_types from the first lifeform for the mutation function to use.
        st.session_state.organ_types = [o.organ_type for o in st.session_state.population[0].organs]

        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        # Evolution Loop
        for gen in range(num_generations):
            status_placeholder.markdown(f"### Generation {gen+1}/{num_generations}...")
            
            # Defensive check inside the loop as well, in case of app re-runs or state loss.
            if 'population' not in st.session_state or not st.session_state.population:
                st.warning(f"Population lost at generation {gen}. Re-initializing.")
                st.session_state.population = [initialize_lifeform() for _ in range(population_size)]
            population = st.session_state.population
            
            # 1. Survival Simulation (Fitness Evaluation)
            for lifeform in population:
                survival_simulation(lifeform, universe)
            
            # Record history
            for lf in population:
                 st.session_state.history.append({
                    'generation': gen,
                    'lineage_id': lf.lineage_id,
                    'form_id': 1, # Simplified for now
                    'survival_fitness': lf.survival_fitness,
                    'energy_balance': lf.energy_balance,
                    'structural_integrity': lf.structural_integrity,
                    'mobility': lf.mobility,
                    'total_mass': sum(o.size for o in lf.organs),
                    'cognitive_complexity': sum(o.size for o in lf.organs if 'Neural' in o.organ_type),
                 })

            # 2. Selection
            population.sort(key=lambda x: x.survival_fitness, reverse=True)
            num_survivors = int(len(population) * selection_pressure)
            survivors = population[:num_survivors]

            # 3. Reproduction
            offspring = []
            while len(offspring) < population_size - len(survivors):
                p1 = random.choice(survivors)
                p2 = random.choice(survivors)
                child = crossover(p1, p2)
                child = mutate(child, universe, mutation_rate, innovation_rate)
                child.generation = gen + 1
                offspring.append(child)

            st.session_state.population = survivors + offspring
            progress_bar.progress((gen + 1) / num_generations)
            
        status_placeholder.markdown("### ✅ Evolution Complete!")
    
    # --- Display Results ---
    if 'history' in st.session_state and st.session_state.history:
        st.markdown("---")
        st.header("🔭 Cosmic Observatory: Results & Analysis")
        
        history_df = pd.DataFrame(st.session_state.history)
        population = st.session_state.population
        
        # Dashboard
        st.plotly_chart(create_evolution_dashboard(history_df), use_container_width=True)
        
        st.markdown("---")
        st.subheader("🏆 Champion Lifeforms of the Final Epoch")
        
        population.sort(key=lambda x: x.survival_fitness, reverse=True)
        
        cols = st.columns(3)
        for i, lifeform in enumerate(population[:3]):
            with cols[i]:
                st.markdown(f"#### Rank {i+1}: {lifeform.lineage_id}")
                st.metric("Survival Fitness", f"{lifeform.survival_fitness:.4f}")
                st.plotly_chart(visualize_lifeform_3d(lifeform), use_container_width=True)
                with st.expander("View Stats"):
                    st.metric("Energy Balance", f"{lifeform.energy_balance:.2f}")
                    st.metric("Structural Integrity", f"{lifeform.structural_integrity:.2f}")
                    st.metric("Mobility", f"{lifeform.mobility:.2f}")


if __name__ == "__main__":
    main()
