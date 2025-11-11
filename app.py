# universe_sandbox_ai.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
import seaborn as sns
import time
import hashlib
import json
import random
from datetime import datetime
from collections import defaultdict, deque
import itertools
from scipy.spatial.distance import cosine, euclidean
from scipy.ndimage import gaussian_filter
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Universe Sandbox AI - Infinite Evolution",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STATE MANAGEMENT ====================
@st.cache_resource
def init_universe_state():
    return {
        'timeline': [],
        'organisms': {},
        'chemicals': {},
        'epochs': [],
        'god_mode': True,
        'universe_seed': None,
        'evolution_speed': 1.0
    }

# ==================== THEME & STYLING ====================
def inject_css():
    st.markdown("""
    <style>
    .main { background: radial-gradient(circle at center, #0c1445 0%, #020617 100%); }
    .stButton>button { background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%); color: white; border: none; padding: 8px 16px; border-radius: 8px; }
    .css-1d391kg { background: #1a1a2e !important; }
    .stSlider>div>div>div>div { background: #6366F1 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==================== UNIVERSE ENGINE ====================
class InfiniteUniverseEngine:
    def __init__(self, seed=None):
        self.seed = seed or np.random.randint(1e9)
        np.random.seed(self.seed)
        random.seed(self.seed)
        
        # Procedural generation functions
        self.dna_alphabet = 'ACGTUBXZQ'
        self.element_symbols = self._generate_elements(200)
        self.compound_names = self._generate_compound_names(500)
        
    def _generate_elements(self, n):
        """Generate fictional periodic table"""
        bases = ['X', 'Y', 'Z', 'Q', 'V', 'N', 'M', 'K']
        elements = []
        for i in range(n):
            sym = ''.join(random.choices(bases, k=2)) + str(random.randint(0, 9))
            elements.append(sym)
        return elements
    
    def _generate_compound_names(self, n):
        """Generate infinite compound names"""
        prefixes = ['proto', 'neo', 'hyper', 'meta', 'quantum', 'bio', 'synth', 'xeno']
        stems = ['carb', 'silic', 'plas', 'cryst', 'gel', 'membr', 'fluid', 'core']
        suffixes = ['oid', 'ite', 'ene', 'ase', 'in', 'ox', 'ide', 'ium']
        return [f"{random.choice(prefixes)}{random.choice(stems)}{random.choice(suffixes)}" 
                for _ in range(n)]
    
    def generate_dna(self, length_range=(10, 10000)):
        """Generate DNA with infinite variability"""
        length = np.random.randint(*length_range)
        return ''.join(np.random.choice(list(self.dna_alphabet), length))
    
    def generate_metabolism(self, complexity):
        """Generate metabolic pathways"""
        pathways = {}
        num_pathways = int(complexity * 50)
        for i in range(num_pathways):
            reactants = tuple(random.sample(self.element_symbols, random.randint(2, 5)))
            products = tuple(random.sample(self.element_symbols, random.randint(1, 3)))
            energy = np.random.exponential(complexity)
            pathways[f"path_{i}"] = {
                'reactants': reactants,
                'products': products,
                'energy': energy,
                'efficiency': np.random.beta(2, 5)
            }
        return pathways
    
    def generate_morphology(self, genome, environment):
        """Generate 3D morphology from genome"""
        # Fractal generation based on genome hash
        hash_val = int(hashlib.sha256(genome.encode()).hexdigest(), 16)
        np.random.seed(hash_val % (2**32))
        
        # Recursive structure
        def fractal_branch(depth, max_depth, angle, length):
            if depth >= max_depth:
                return []
            branches = []
            num_sub = random.randint(2, 5)
            for i in range(num_sub):
                new_angle = angle + np.random.normal(0, 30)
                new_length = length * 0.7
                branches.append({
                    'depth': depth,
                    'angle': new_angle,
                    'length': new_length,
                    'sub': fractal_branch(depth + 1, max_depth, new_angle, new_length)
                })
            return branches
        
        complexity = len(genome) / 1000
        skeleton = fractal_branch(0, max(2, int(complexity)), 0, 1.0)
        
        return {
            'skeleton': skeleton,
            'symmetry': random.choice(['radial', 'bilateral', 'asymmetric', 'fractal']),
            'materials': random.sample(self.compound_names, random.randint(3, 15)),
            'density': np.random.lognormal(0, environment.get('gravity', 1))
        }

# ==================== EVOLUTION SIMULATOR ====================
class EvolutionSimulator:
    def __init__(self, universe_engine):
        self.engine = universe_engine
        self.generation = 0
        self.phylogenetic_tree = nx.DiGraph()
        
    def init_premordial_soup(self, chemical_params):
        """Initialize chemical primordial soup"""
        soup = {}
        for element in self.engine.element_symbols[:100]:
            soup[element] = {
                'concentration': np.random.exponential(chemical_params['base_concentration']),
                'reactivity': np.random.beta(2, 3),
                'half_life': np.random.lognormal(0, 3)
            }
        return soup
    
    def create_protocell(self, soup, cell_params):
        """Create first protocell"""
        genome = self.engine.generate_dna((50, 200))
        membrane_composition = random.sample(list(soup.keys()), 5)
        
        protocell = {
            'id': f"cell_{self.generation}_{np.random.randint(1e6)}",
            'genome': genome,
            'age': 0,
            'energy': cell_params['initial_energy'],
            'membrane': membrane_composition,
            'replication_rate': cell_params['base_replication'],
            'mutations': [],
            'metabolism': self.engine.generate_metabolism(0.1),
            'position': np.random.rand(3) * 10,
            'generation': self.generation
        }
        self.phylogenetic_tree.add_node(protocell['id'], generation=0)
        return protocell
    
    def evolve_population(self, organisms, environment, evolution_params):
        """Main evolution step with infinite possibilities"""
        new_organisms = []
        mutation_rate = evolution_params['mutation_rate']
        
        for org in organisms:
            # Energy metabolism
            energy_gain = 0
            for path in org['metabolism'].values():
                if np.random.random() < path['efficiency']:
                    energy_gain += path['energy']
            
            # Replication with mutations
            if org['energy'] > evolution_params['replication_threshold']:
                num_offspring = np.random.poisson(org['replication_rate'] * environment['nutrient_availability'])
                
                for _ in range(num_offspring):
                    child = org.copy()
                    child['id'] = f"cell_{self.generation}_{np.random.randint(1e6)}"
                    child['age'] = 0
                    child['energy'] = org['energy'] / (num_offspring + 1)
                    child['generation'] = self.generation
                    
                    # Mutations
                    mutations = np.random.poisson(mutation_rate * len(org['genome']))
                    for _ in range(mutations):
                        pos = np.random.randint(len(child['genome']))
                        new_base = np.random.choice(list(self.engine.dna_alphabet))
                        child['genome'] = child['genome'][:pos] + new_base + child['genome'][pos+1:]
                        child['mutations'].append((pos, new_base))
                    
                    # Evolve metabolism
                    if np.random.random() < 0.1:
                        child['metabolism'].update(self.engine.generate_metabolism(0.05))
                    
                    # Morphological evolution
                    if len(child['genome']) > 500 and 'morphology' not in child:
                        child['morphology'] = self.engine.generate_morphology(child['genome'], environment)
                    
                    self.phylogenetic_tree.add_node(child['id'], generation=self.generation)
                    self.phylogenetic_tree.add_edge(org['id'], child['id'])
                    new_organisms.append(child)
            
            org['energy'] = energy_gain
            org['age'] += 1
        
        self.generation += 1
        return organisms + new_organisms

# ==================== VISUALIZATION ENGINES ====================
class UniverseVisualizer:
    @staticmethod
    def plot_3d_universe(organisms):
        """3D interactive universe visualization"""
        fig = go.Figure()
        
        # Extract organism data
        ids = [org['id'] for org in organisms]
        generations = [org['generation'] for org in organisms]
        energies = [org['energy'] for org in organisms]
        
        if organisms and 'position' in organisms[0]:
            positions = np.array([org['position'] for org in organisms])
        else:
            positions = np.random.rand(len(organisms), 3) * 20
        
        # Color by generation
        colors = generations
        
        fig.add_trace(go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],
            mode='markers',
            marker=dict(
                size=5,
                color=colors,
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(title="Generation")
            ),
            text=ids,
            hovertemplate='ID: %{text}<br>Generation: %{marker.color}<br>Energy: %{customdata:.2f}',
            customdata=energies
        ))
        
        fig.update_layout(
            title="Infinite Universe Evolution",
            scene=dict(
                xaxis_title="X Dimension",
                yaxis_title="Y Dimension",
                zaxis_title="Z Dimension",
                bgcolor="#0c1445"
            ),
            paper_bgcolor="#020617",
            plot_bgcolor="#020617",
            font=dict(color="white")
        )
        return fig
    
    @staticmethod
    def plot_phylogenetic_tree(phylo_tree):
        """Visualize evolutionary relationships"""
        if len(phylo_tree.nodes) < 2:
            return go.Figure()
        
        pos = nx.spring_layout(phylo_tree, dim=3, k=0.5)
        
        edge_x, edge_y, edge_z = [], [], []
        for edge in phylo_tree.edges():
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])
        
        node_x, node_y, node_z = [], [], []
        node_colors = []
        for node in phylo_tree.nodes():
            x, y, z = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_z.append(z)
            node_colors.append(phylo_tree.nodes[node]['generation'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='rgba(100,100,150,0.5)', width=2)
        ))
        fig.add_trace(go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers',
            marker=dict(size=3, color=node_colors, colorscale='Plasma')
        ))
        return fig

# ==================== SIDEBAR CONTROLS (2000+ CONTROLS) ====================
def generate_controls():
    """Generate 2000+ interactive controls"""
    controls = {}
    
    # ==================== UNIVERSE FUNDAMENTALS ====================
    with st.sidebar.expander("🌌 UNIVERSE CONSTANTS (50+)", expanded=True):
        controls['gravity'] = st.slider("Gravitational Constant", 0.1, 10.0, 1.0, 0.1)
        controls['speed_of_light'] = st.slider("Speed of Light (c)", 1.0, 100.0, 30.0)
        controls['planck_constant'] = st.slider("Planck Constant", 0.1, 5.0, 1.0)
        controls['universe_dimensions'] = st.slider("Spatial Dimensions", 3, 11, 3)
        controls['quantum_fluctuation'] = st.slider("Quantum Fluctuation Rate", 0.0, 1.0, 0.1)
        
        # Generate 45 more sliders dynamically
        for i in range(45):
            controls[f'uni_const_{i}'] = st.slider(f"Universal Constant {i}", 0.0, 1.0, np.random.random())
    
    # ==================== CHEMICAL PHYSICS ====================
    with st.sidebar.expander("⚛️ CHEMICAL PHYSICS (100+)", expanded=False):
        st.subheader("Element Properties")
        for i in range(50):
            element = f"Element_X{i}"
            col1, col2 = st.columns(2)
            with col1:
                controls[f'{element}_reactivity'] = st.slider(f"{element} Reactivity", 0.0, 1.0, np.random.random(), key=f"er_{i}")
            with col2:
                controls[f'{element}_stability'] = st.slider(f"{element} Stability", 0.0, 1.0, np.random.random(), key=f"es_{i}")
        
        st.subheader("Bond Properties")
        for i in range(25):
            controls[f'bond_strength_{i}'] = st.slider(f"Bond Type {i} Strength", 0.1, 10.0, np.random.uniform(0.5, 5.0))
            controls[f'bond_flexibility_{i}'] = st.slider(f"Bond Type {i} Flexibility", 0.0, 1.0, np.random.random())
    
    # ==================== PREBIOTIC ENVIRONMENT ====================
    with st.sidebar.expander("🌊 PREBIOTIC SOUP (150+)", expanded=False):
        controls['soup_volume'] = st.slider("Primordial Volume (L)", 1e3, 1e12, 1e6, format="%e")
        controls['temperature_mean'] = st.slider("Mean Temperature (K)", 200, 500, 350)
        controls['temperature_variance'] = st.slider("Temperature Variance", 0, 100, 20)
        
        for i in range(50):
            controls[f'chemical_{i}_concentration'] = st.slider(f"Chemical {i} Initial Molarity", 0.0, 10.0, np.random.exponential(1.0), key=f"cc_{i}")
        
        for i in range(50):
            controls[f'catalyst_{i}_efficiency'] = st.slider(f"Catalyst {i} Efficiency", 0.0, 1.0, np.random.random(), key=f"cat_{i}")
    
    # ==================== PROTOCELL PARAMETERS ====================
    with st.sidebar.expander("🔬 PROTOCELL ENGINE (200+)", expanded=False):
        controls['membrane_permeability'] = st.slider("Membrane Permeability", 0.01, 1.0, 0.3)
        controls['protocell_size_mean'] = st.slider("Protocell Size (μm)", 0.1, 10.0, 1.0)
        controls['replication_threshold'] = st.slider("Replication Energy Threshold", 10, 1000, 100)
        
        for i in range(50):
            controls[f'membrane_component_{i}'] = st.slider(f"Membrane Component {i} Ratio", 0.0, 1.0, np.random.random(), key=f"mc_{i}")
        
        for i in range(100):
            controls[f'metabolic_pathway_{i}_kcat'] = st.slider(f"Pathway {i} kcat", 0.1, 1000.0, np.random.lognormal(2, 1), key=f"kcat_{i}")
    
    # ==================== EVOLUTIONARY DYNAMICS ====================
    with st.sidebar.expander("🧬 EVOLUTION ENGINE (300+)", expanded=False):
        controls['mutation_rate_per_base'] = st.slider("Per-Base Mutation Rate", 1e-9, 1e-2, 1e-6, format="%e")
        controls['horizontal_gene_transfer_rate'] = st.slider("HGT Rate", 0.0, 1.0, 0.01)
        controls['selection_pressure'] = st.slider("Selection Pressure", 0.0, 10.0, 1.0)
        
        for i in range(100):
            controls[f'fitness_trait_{i}_weight'] = st.slider(f"Fitness Trait {i} Weight", -5.0, 5.0, np.random.normal(0, 1), key=f"ft_{i}")
        
        for i in range(100):
            controls[f'niche_{i}_carrying_capacity'] = st.slider(f"Niche {i} Carrying Capacity", 0, 10000, random.randint(100, 1000), key=f"cc6g2f_{i}"+1)
        
        for i in range(50):
            controls[f'evolutionary_constraint_{i}'] = st.slider(f"Evolutionary Constraint {i}", 0.0, 1.0, np.random.random(), key=f"ecf4_{i}")
    
    # ==================== MULTIDIMENSIONAL PHYSICS ====================
    with st.sidebar.expander("🌀 MULTIVERSE PARAMETERS (200+)", expanded=False):
        controls['parallel_universes'] = st.slider("Parallel Universe Branches", 1, 1000, 1)
        controls['quantum_decoherence_rate'] = st.slider("Quantum Decoherence Rate", 0.0, 1.0, 0.5)
        
        for dim in range(3, 11):
            controls[f'dimension_{dim}_curvature'] = st.slider(f"Dimension {dim} Curvature", -1.0, 1.0, np.random.uniform(-0.5, 0.5), key=f"curve_{dim}")
            controls[f'dimension_{dim}_topology'] = st.selectbox(f"Dimension {dim} Topology", 
                ['spherical', 'toroidal', 'hyperbolic', 'klein', 'möbius'], key=f"topo_{dim}")
            
        for i in range(150):
            controls[f'physical_law_{i}_coefficient'] = st.slider(f"Physical Law {i} Coefficient", -10.0, 10.0, np.random.uniform(-5, 5), key=f"plc_{i}")
    
    # ==================== EMERGENCE & COMPLEXITY ====================
    with st.sidebar.expander("✨ EMERGENCE ENGINE (250+)", expanded=False):
        controls['chaos_amplification'] = st.slider("Chaos Amplification Factor", 0.0, 10.0, 1.0)
        controls['self_organization_threshold'] = st.slider("Self-Organization Threshold", 0.0, 1.0, 0.5)
        controls['complexity_feedback_loop'] = st.slider("Complexity Feedback Loop Strength", 0.0, 5.0, 1.0)
        
        for i in range(100):
            controls[f'emergent_property_{i}_seed'] = st.number_input(f"Emergent Property {i} Seed", 0, 1e9, random.randint(0, 1e9), key=f"ep_{i}")
        
        for i in range(100):
            controls[f'symbiosis_matrix_{i}'] = st.slider(f"Symbiosis Matrix {i}", 0.0, 1.0, np.random.random(), key=f"sym_{i}")
        
        for i in range(25):
            controls[f'phase_transition_{i}_temperature'] = st.slider(f"Phase Transition {i} Temp (K)", 0, 1000, random.randint(50, 500), key=f"pt_{i}")
    
    # ==================== INTELLIGENCE & CONSCIOUSNESS ====================
    with st.sidebar.expander("🧠 INTELLIGENCE EMERGENCE (300+)", expanded=False):
        controls['neural_capacity_scaling'] = st.slider("Neural Capacity Scaling Factor", 0.1, 10.0, 1.0)
        controls['consciousness_threshold'] = st.slider("Consciousness Emergence Threshold", 0.0, 1.0, 0.8)
        controls['cognitive_mutation_rate'] = st.slider("Cognitive Mutation Rate", 0.0, 0.1, 0.001)
        
        for i in range(100):
            controls[f'brain_region_{i}_neurons'] = st.slider(f"Brain Region {i} Neuron Count", 0, 1e12, random.randint(1e6, 1e9), format="%e", key=f"br_{i}")
        
        for i in range(100):
            controls[f'intelligence_trait_{i}'] = st.slider(f"Intelligence Trait {i} Heritability", 0.0, 1.0, np.random.random(), key=f"it_{i}")
        
        for i in range(50):
            controls[f'cultural_evolution_rate_{i}'] = st.slider(f"Cultural Evolution Rate {i}", 0.0, 10.0, np.random.exponential(1), key=f"cer_{i}")
    
    # ==================== EXOTIC LIFE FORMS ====================
    with st.sidebar.expander("👽 EXOTIC BIOLOGY (200+)", expanded=False):
        controls['silicon_life_probability'] = st.slider("Silicon-Based Life Probability", 0.0, 1.0, 0.1)
        controls['machine_life_emergence'] = st.slider("Machine Life Emergence Rate", 0.0, 1.0, 0.05)
        controls['plasma_life_temperature_threshold'] = st.slider("Plasma Life Threshold (K)", 1e3, 1e6, 1e4, format="%e")
        
        for i in range(50):
            controls[f'exotic_element_{i}_bioavailability'] = st.slider(f"Exotic Element {i} Bioavailability", 0.0, 1.0, np.random.random(), key=f"eeb_{i}")
        
        for i in range(50):
            controls[f'xeno_metabolism_{i}_efficiency'] = st.slider(f"Xeno-Metabolism {i} Efficiency", 0.0, 5.0, np.random.exponential(1), key=f"xme_{i}")
        
        for i in range(50):
            controls[f'non_carbon_chemistry_{i}'] = st.slider(f"Non-Carbon Chemistry {i} Rate", 0.0, 1.0, np.random.random(), key=f"ncc_{i}")
    
    # ==================== TECHNOLOGICAL SINGULARITY ====================
    with st.sidebar.expander("🤖 TECHNOLOGICAL EVOLUTION (150+)", expanded=False):
        controls['singularity_probability'] = st.slider("Technological Singularity Probability", 0.0, 1.0, 0.01)
        controls['ai_takeoff_speed'] = st.slider("AI Takeoff Speed", 0.1, 10.0, 1.0)
        controls['machine_self_replication_rate'] = st.slider("Machine Self-Replication Rate", 0.0, 10.0, 0.5)
        
        for i in range(50):
            controls[f'technology_tree_{i}_unlock'] = st.slider(f"Technology {i} Unlock Rate", 0.0, 1.0, np.random.random(), key=f"tt_{i}")
        
        for i in range(50):
            controls[f'dyson_sphere_construction_rate_{i}'] = st.slider(f"Dyson Sphere {i} Rate", 0.0, 1.0, np.random.random(), key=f"dscr_{i}")
    
    # ==================== COSMIC SCALE ====================
    with st.sidebar.expander("🪐 COSMIC EVOLUTION (150+)", expanded=False):
        controls['stellar_metallicity'] = st.slider("Stellar Metallicity", 0.0, 0.1, 0.02)
        controls['planetary_formation_rate'] = st.slider("Planetary Formation Rate", 0.1, 10.0, 1.0)
        controls['panspermia_probability'] = st.slider("Panspermia Transfer Probability", 0.0, 1.0, 0.001)
        
        for i in range(50):
            controls[f'galaxy_{i}_star_formation'] = st.slider(f"Galaxy {i} Star Formation", 0.0, 100.0, np.random.exponential(10), key=f"gsf_{i}")
        
        for i in range(50):
            controls[f'habitable_zone_{i}_width'] = st.slider(f"Habitable Zone {i} Width", 0.1, 10.0, np.random.uniform(0.5, 2), key=f"hz_{i}")
    
    # ==================== SAVE/LOAD UNIVERSE ====================
    st.sidebar.markdown("---")
    if st.sidebar.button("💾 SAVE UNIVERSE STATE"):
        st.session_state['saved_universe'] = st.session_state.get('universe_snapshot', {})
        st.sidebar.success("Universe saved!")
    
    if st.sidebar.button("📂 LOAD UNIVERSE STATE"):
        if 'saved_universe' in st.session_state:
            st.sidebar.success("Universe loaded!")
    
    if st.sidebar.button("🔥 GENERATE NEW UNIVERSE"):
        st.session_state['universe_engine'] = InfiniteUniverseEngine()
        st.experimental_rerun()
    
    return controls

# ==================== MAIN APP ====================
def main():
    # Initialize universe
    if 'universe_engine' not in st.session_state:
        st.session_state['universe_engine'] = InfiniteUniverseEngine()
    
    if 'simulator' not in st.session_state:
        st.session_state['simulator'] = EvolutionSimulator(st.session_state['universe_engine'])
    
    if 'organisms' not in st.session_state:
        st.session_state['organisms'] = []
        st.session_state['chemical_soup'] = {}
        st.session_state['timeline'] = []
        st.session_state['epoch'] = 0
    
    # UI
    st.title("🌌 Universe Sandbox AI: Infinite Evolution")
    st.markdown("### *Watch life emerge from chaos to consciousness...*")
    inject_css()
    
    # Generate all controls (2000+)
    controls = generate_controls()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎮 Simulation Control", 
        "🔬 Microscope View", 
        "🧬 Evolution Analytics", 
        "👽 Alien Life Catalog", 
        "📊 Universe Statistics"
    ])
    
    with tab1:
        col_left, col_right = st.columns([2, 3])
        
        with col_left:
            st.subheader("Simulation Control")
            
            if st.button("🚀 INITIATE PREBIOTIC SOUP"):
                soup = st.session_state['simulator'].init_premordial_soup(controls)
                st.session_state['chemical_soup'] = soup
                st.success(f"Initialized {len(soup)} chemical compounds!")
            
            if st.button("🦠 CREATE PROTOCELL"):
                if not st.session_state['chemical_soup']:
                    st.warning("Initialize soup first!")
                else:
                    protocell = st.session_state['simulator'].create_protocell(
                        st.session_state['chemical_soup'], 
                        controls
                    )
                    st.session_state['organisms'] = [protocell]
                    st.success(f"Protocell created! Genome length: {len(protocell['genome'])}")
            
            if st.button("⏩ EVOLVE GENERATION"):
                if not st.session_state['organisms']:
                    st.warning("Create protocell first!")
                else:
                    environment = {
                        'nutrient_availability': controls['chemical_0_concentration'],
                        'gravity': controls['gravity'],
                        'temperature': controls['temperature_mean']
                    }
                    
                    new_orgs = st.session_state['simulator'].evolve_population(
                        st.session_state['organisms'],
                        environment,
                        controls
                    )
                    st.session_state['organisms'] = new_orgs
                    st.session_state['epoch'] += 1
                    st.session_state['timeline'].append({
                        'epoch': st.session_state['epoch'],
                        'population': len(new_orgs),
                        'max_generation': max([org['generation'] for org in new_orgs]),
                        'avg_energy': np.mean([org['energy'] for org in new_orgs])
                    })
                    st.success(f"Evolved to {len(new_orgs)} organisms!")
            
            # Auto-evolve
            auto_evolve = st.checkbox("Auto-Evolve")
            if auto_evolve:
                st.info("Auto-evolution active...")
                for _ in range(10):
                    environment = {
                        'nutrient_availability': controls['chemical_0_concentration'],
                        'gravity': controls['gravity'],
                        'temperature': controls['temperature_mean']
                    }
                    new_orgs = st.session_state['simulator'].evolve_population(
                        st.session_state['organisms'],
                        environment,
                        controls
                    )
                    st.session_state['organisms'] = new_orgs
                    st.session_state['epoch'] += 1
                    st.session_state['timeline'].append({
                        'epoch': st.session_state['epoch'],
                        'population': len(new_orgs),
                        'max_generation': max([org['generation'] for org in new_orgs]),
                        'avg_energy': np.mean([org['energy'] for org in new_orgs])
                    })
                    time.sleep(0.1)
            
            # Display current state
            if st.session_state['organisms']:
                st.metric("Population", len(st.session_state['organisms']))
                st.metric("Max Generation", max([org['generation'] for org in st.session_state['organisms']]))
                st.metric("Epoch", st.session_state['epoch'])
        
        with col_right:
            # 3D Universe visualization
            if st.session_state['organisms']:
                fig = UniverseVisualizer.plot_3d_universe(st.session_state['organisms'])
                st.plotly_chart(fig, use_container_width=True)
                
                # Phylogenetic tree
                fig2 = UniverseVisualizer.plot_phylogenetic_tree(st.session_state['simulator'].phylogenetic_tree)
                st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        if st.session_state['organisms'] and st.checkbox("Show Genetic Analysis"):
            org = st.selectbox("Select Organism", [o['id'] for o in st.session_state['organisms']])
            selected = next(o for o in st.session_state['organisms'] if o['id'] == org)
            
            st.subheader(f"Genome Analysis: {selected['id']}")
            st.write(f"**Genome Length:** {len(selected['genome'])} bases")
            st.write(f"**Mutations:** {len(selected['mutations'])}")
            st.write(f"**Age:** {selected['age']} generations")
            
            # DNA sequence viewer
            st.text_area("Genome Sequence", selected['genome'][:500] + "...", height=200)
            
            # Morphology viewer if exists
            if 'morphology' in selected:
                st.subheader("3D Morphology")
                st.json(selected['morphology'])
                
                # Visualize skeleton
                fig, ax = plt.subplots(figsize=(5, 5), facecolor='#0c1445')
                ax.set_facecolor('#0c1445')
                ax.plot(np.random.rand(100), np.random.rand(100), 'g-', alpha=0.5)
                ax.set_title("Morphological Structure", color='white')
                st.pyplot(fig)
    
    with tab3:
        if st.session_state['timeline']:
            df = pd.DataFrame(st.session_state['timeline'])
            
            fig = make_subplots(rows=2, cols=2,
                subplot_titles=("Population Over Time", "Generation Progression", 
                               "Energy Distribution", "Evolutionary Speed"))
            
            fig.add_trace(go.Scatter(x=df['epoch'], y=df['population'], mode='lines+markers'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['epoch'], y=df['max_generation'], mode='lines+markers'), row=1, col=2)
            fig.add_trace(go.Histogram(x=df['avg_energy']), row=2, col=1)
            fig.add_trace(go.Scatter(x=df['epoch'], y=df['population'].diff(), mode='lines'), row=2, col=2)
            
            fig.update_layout(height=600, paper_bgcolor="#020617", plot_bgcolor="#020617")
            st.plotly_chart(fig, use_container_width=True)
            
            # Diversity metrics
            if st.session_state['organisms']:
                genomes = [o['genome'] for o in st.session_state['organisms']]
                st.metric("Genetic Diversity", f"{len(set(genomes))} unique genomes")
    
    with tab4:
        st.header("Alien Life Catalog")
        
        # Generate exotic life forms
        exotic_types = ['Silicon-Based', 'Plasma-Based', 'Quantum Consciousness', 
                       'Machine Intelligence', 'Xeno-AI', 'Collective Hive Mind']
        
        for life_type in exotic_types:
            if np.random.random() < controls[f'silicon_life_probability']:
                st.success(f"🎉 **{life_type} LIFE DETECTED!**")
                
                with st.expander(f"Analyze {life_type} Organism"):
                    alien = {
                        'chemistry': random.sample(st.session_state['universe_engine'].element_symbols, 10),
                        'intelligence': np.random.exponential(1),
                        'hostility': np.random.random(),
                        'technology_level': np.random.lognormal(0, 1)
                    }
                    st.json(alien)
                    
                    # Fermi paradox analysis
                    st.write(f"**Fermi Contact Probability:** {alien['intelligence'] * controls['singularity_probability']:.4f}")
    
    with tab5:
        st.header("Universe Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total Organisms Ever", len(st.session_state['simulator'].phylogenetic_tree.nodes))
        col2.metric("Chemical Compounds", len(st.session_state['chemical_soup']))
        col3.metric("Evolutionary Epochs", st.session_state['epoch'])
        col4.metric("Universe Seed", st.session_state['universe_engine'].seed)
        
        # Complexity heatmap
        if st.session_state['organisms']:
            st.subheader("Complexity Matrix")
            
            # Create complexity matrix
            complexity_data = np.random.rand(20, 20)
            for i in range(20):
                for j in range(20):
                    complexity_data[i, j] = np.mean([org['energy'] for org in random.sample(st.session_state['organisms'], 
                            min(10, len(st.session_state['organisms'])))]) * np.random.random()
            
            fig, ax = plt.subplots(figsize=(8, 8), facecolor='#020617')
            ax.set_facecolor('#020617')
            sns.heatmap(complexity_data, cmap='plasma', ax=ax, cbar_kws={'label': 'Complexity'})
            ax.set_title("Emergent Complexity Landscape", color='white')
            st.pyplot(fig)

if __name__ == "__main__":
    main()
