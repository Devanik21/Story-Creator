# Create a new file named UniverseSandboxAI.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
import random
import time
import uuid
from collections import Counter
import json
import math

# ==============================================================================
# 1. UNIVERSE CONSTANTS & PHYSICS ENGINE
# ==============================================================================
# These classes define the fundamental, unchangeable laws of your universe.
# Once the simulation starts, these are fixed.

@dataclass
class PhysicsConstants:
    """Defines the physical laws of the universe."""
    gravity: float = 0.01
    friction: float = 0.95
    max_velocity: float = 1.0
    time_step: float = 1.0
    interaction_radius: float = 5.0  # Radius for local interactions
    bond_force: float = 0.1  # Force keeping bonded particles together
    repulsion_force: float = 0.5 # Force preventing particle overlap

@dataclass
class Element:
    """Defines a fundamental building block of matter."""
    id: int
    name: str
    color: str
    mass: float
    max_bonds: int
    properties: Set[str] = field(default_factory=set) # e.g., 'photosynthetic', 'conductive'

@dataclass
class Chemistry:
    """Defines the rules of bonding and reactions."""
    elements: List[Element]
    # Defines how strongly elements bond. Higher number = stronger bond.
    # Key is a sorted tuple of element IDs.
    bond_strengths: Dict[Tuple[int, int], float] = field(default_factory=dict)
    # Defines reactions, e.g., what happens when particles meet.
    reactions: Dict[str, str] = field(default_factory=dict)

# ==============================================================================
# 2. GENETIC & PHENOTYPIC REPRESENTATION
# ==============================================================================
# This is the core of life: the genetic code and the physical body it creates.

@dataclass
class Particle:
    """A single point of matter in an organism's body."""
    id: str
    element_id: int
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    charge: float = 0.0 # Represents stored energy
    age: int = 0

@dataclass
class Bond:
    """A connection between two particles."""
    p1_id: str
    p2_id: str
    strength: float

@dataclass
class Genome:
    """
    The genetic blueprint of an organism. It's a Turing-complete "tape" of instructions
    that dictates how the organism builds itself.
    """
    # Instruction tape, e.g., [ADD_PARTICLE(C), MOVE(NORTH), BOND, LOOP_START, ...]
    tape: List[Dict] = field(default_factory=list)
    lineage_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None
    generation: int = 0
    
    def copy(self):
        return Genome(
            tape=[i.copy() for i in self.tape],
            parent_id=self.lineage_id,
            generation=self.generation
        )

@dataclass
class Organism:
    """The physical manifestation (phenotype) of a genome."""
    genome: Genome
    particles: Dict[str, Particle] = field(default_factory=dict)
    bonds: List[Bond] = field(default_factory=list)
    fitness: float = 0.0
    age: int = 0
    energy: float = 100.0 # Starting energy
    is_alive: bool = True
    
    # Metrics
    size: int = 0
    mass: float = 0.0
    structural_integrity: float = 0.0
    mobility: float = 0.0 # How much it moves

# ==============================================================================
# 3. THE SIMULATION ENGINE
# ==============================================================================
# These functions govern the lifecycle of the universe: birth, life, and death.

def get_element_by_id(element_id: int, chemistry: Chemistry) -> Optional[Element]:
    """Helper to find an element by its ID."""
    for e in chemistry.elements:
        if e.id == element_id:
            return e
    return None

def run_development(genome: Genome, chemistry: Chemistry) -> Tuple[Dict[str, Particle], List[Bond]]:
    """
    Executes the genetic program to build an organism's body (phenotype).
    This is the "ontogeny" or "growth" phase.
    """
    particles = {}
    bonds = []
    
    # The "developmental machine" state
    pointer = 0
    cursor_x, cursor_y = 0.0, 0.0
    last_particle_id = None
    
    max_steps = 200 # Prevent infinite loops in development
    
    for _ in range(max_steps):
        if pointer >= len(genome.tape):
            break
            
        instruction = genome.tape[pointer]
        cmd = instruction["cmd"]
        
        if cmd == "ADD_PARTICLE":
            element_id = instruction["element_id"]
            element = get_element_by_id(element_id, chemistry)
            if element:
                new_id = str(uuid.uuid4())
                # Check for existing particle at this location
                is_occupied = False
                for p in particles.values():
                    if abs(p.x - cursor_x) < 1 and abs(p.y - cursor_y) < 1:
                        is_occupied = True
                        break
                if not is_occupied:
                    particles[new_id] = Particle(id=new_id, element_id=element.id, x=cursor_x, y=cursor_y)
                    last_particle_id = new_id

        elif cmd == "MOVE":
            direction = instruction["direction"]
            dist = instruction.get("dist", 5.0)
            if direction == "N": cursor_y += dist
            elif direction == "S": cursor_y -= dist
            elif direction == "E": cursor_x += dist
            elif direction == "W": cursor_x -= dist

        elif cmd == "BOND":
            if last_particle_id and instruction["target_id"] in particles:
                p1_id, p2_id = sorted((last_particle_id, instruction["target_id"]))
                p1 = particles[p1_id]
                p2 = particles[p2_id]
                
                # Check bond count
                p1_bonds = sum(1 for b in bonds if b.p1_id == p1_id or b.p2_id == p1_id)
                p2_bonds = sum(1 for b in bonds if b.p1_id == p2_id or b.p2_id == p2_id)
                
                e1 = get_element_by_id(p1.element_id, chemistry)
                e2 = get_element_by_id(p2.element_id, chemistry)

                if e1 and e2 and p1_bonds < e1.max_bonds and p2_bonds < e2.max_bonds:
                    bond_strength_key = tuple(sorted((p1.element_id, p2.element_id)))
                    strength = chemistry.bond_strengths.get(bond_strength_key, 0.1)
                    bonds.append(Bond(p1_id=p1_id, p2_id=p2_id, strength=strength))

        elif cmd == "JUMP_IF_NEAR":
            # A simple conditional for creating complex structures
            is_near = False
            for p in particles.values():
                dist_sq = (p.x - cursor_x)**2 + (p.y - cursor_y)**2
                if dist_sq < 25: # 5 units radius
                    is_near = True
                    break
            if is_near:
                pointer = instruction["target_ptr"] - 1 # -1 to account for pointer increment

        pointer += 1
        
    return particles, bonds

def mutate_genome(genome: Genome, chemistry: Chemistry, settings: Dict) -> Genome:
    """Applies mutations to a genome's instruction tape."""
    mutated = genome.copy()
    
    # Point mutation
    if random.random() < settings['mutation_rate_point'] and mutated.tape:
        idx = random.randint(0, len(mutated.tape) - 1)
        instr = mutated.tape[idx]
        if instr["cmd"] == "ADD_PARTICLE":
            instr["element_id"] = random.choice(chemistry.elements).id
        elif instr["cmd"] == "MOVE":
            instr["direction"] = random.choice(["N", "S", "E", "W"])
    
    # Insertion
    if random.random() < settings['mutation_rate_insertion']:
        idx = random.randint(0, len(mutated.tape))
        # Choose a random new instruction to insert
        new_cmd_type = random.choice(["ADD_PARTICLE", "MOVE", "BOND", "JUMP_IF_NEAR"])
        new_instr = {}
        if new_cmd_type == "ADD_PARTICLE":
            new_instr = {"cmd": "ADD_PARTICLE", "element_id": random.choice(chemistry.elements).id}
        elif new_cmd_type == "MOVE":
            new_instr = {"cmd": "MOVE", "direction": random.choice(["N", "S", "E", "W"])}
        elif new_cmd_type == "BOND":
            # This is tricky, needs a valid target. For now, we simplify.
            # A more complex version would search for a nearby particle ID.
            new_instr = {"cmd": "BOND", "target_id": "find_nearest"} # Placeholder logic
        elif new_cmd_type == "JUMP_IF_NEAR":
             new_instr = {"cmd": "JUMP_IF_NEAR", "target_ptr": random.randint(0, len(mutated.tape))}
        
        if new_instr:
            mutated.tape.insert(idx, new_instr)

    # Deletion
    if random.random() < settings['mutation_rate_deletion'] and len(mutated.tape) > 1:
        idx = random.randint(0, len(mutated.tape) - 1)
        mutated.tape.pop(idx)
        
    # Duplication
    if random.random() < settings['mutation_rate_duplication'] and len(mutated.tape) > 0:
        start = random.randint(0, len(mutated.tape) - 1)
        end = random.randint(start, len(mutated.tape))
        segment = mutated.tape[start:end]
        insert_pos = random.randint(0, len(mutated.tape))
        mutated.tape = mutated.tape[:insert_pos] + segment + mutated.tape[insert_pos:]

    return mutated

def evaluate_fitness(organism: Organism, chemistry: Chemistry, settings: Dict) -> float:
    """Calculates fitness based on structure and properties."""
    if not organism.particles:
        return 0.0

    # 1. Structural Integrity: Bonus for being connected.
    # We can use a simple check: is the structure a single connected component?
    # A more advanced check would be average bond strength.
    num_particles = len(organism.particles)
    num_bonds = len(organism.bonds)
    integrity = (num_bonds / (num_particles - 1)) if num_particles > 1 else 1.0
    integrity = min(1.0, integrity)

    # 2. Metabolic Efficiency: Based on special properties of elements.
    photosynthetic_particles = 0
    for p in organism.particles.values():
        element = get_element_by_id(p.element_id, chemistry)
        if element and 'photosynthetic' in element.properties:
            photosynthetic_particles += 1
    
    energy_generation = (photosynthetic_particles / num_particles) if num_particles > 0 else 0.0

    # 3. Size & Complexity: Penalize being too large or too small.
    # Optimal size is a setting.
    size_fitness = 1.0 - abs(num_particles - settings['optimal_organism_size']) / settings['optimal_organism_size']
    size_fitness = max(0, size_fitness)

    # 4. Mobility: Reward movement.
    mobility_fitness = min(1.0, organism.mobility / 10.0)

    # Combine objectives with weights
    total_fitness = (
        integrity * settings['w_integrity'] +
        energy_generation * settings['w_energy_generation'] +
        size_fitness * settings['w_size'] +
        mobility_fitness * settings['w_mobility']
    )
    
    return max(1e-6, total_fitness)

def update_world(organisms: List[Organism], resources: np.ndarray, physics: PhysicsConstants, chemistry: Chemistry, settings: Dict):
    """The main simulation loop for one time step."""
    width, height = resources.shape
    
    for org in organisms:
        if not org.is_alive:
            continue

        # --- Physics Simulation ---
        total_dx, total_dy = 0, 0
        
        # Apply forces
        for bond in org.bonds:
            p1 = org.particles.get(bond.p1_id)
            p2 = org.particles.get(bond.p2_id)
            if not p1 or not p2: continue

            dx, dy = p2.x - p1.x, p2.y - p1.y
            dist = math.sqrt(dx**2 + dy**2) + 1e-6
            
            # Ideal distance is based on element size (simplified here)
            ideal_dist = 5.0
            force_mag = (dist - ideal_dist) * physics.bond_force * bond.strength
            
            force_x, force_y = (dx / dist) * force_mag, (dy / dist) * force_mag
            p1.vx += force_x
            p1.vy += force_y
            p2.vx -= force_x
            p2.vy -= force_y

        # Repulsion from other particles in the same organism
        particle_list = list(org.particles.values())
        for i in range(len(particle_list)):
            for j in range(i + 1, len(particle_list)):
                p1, p2 = particle_list[i], particle_list[j]
                dx, dy = p2.x - p1.x, p2.y - p1.y
                dist_sq = dx**2 + dy**2
                if 0 < dist_sq < physics.interaction_radius**2:
                    dist = math.sqrt(dist_sq)
                    force_mag = (1.0 / dist) * physics.repulsion_force
                    force_x, force_y = (dx / dist) * force_mag, (dy / dist) * force_mag
                    p1.vx -= force_x
                    p1.vy -= force_y
                    p2.vx += force_x
                    p2.vy += force_y

        # Update positions
        center_x, center_y = 0, 0
        for p in org.particles.values():
            # Gravity
            p.vy -= physics.gravity
            
            # Friction
            p.vx *= physics.friction
            p.vy *= physics.friction
            
            # Clamp velocity
            p.vx = np.clip(p.vx, -physics.max_velocity, physics.max_velocity)
            p.vy = np.clip(p.vy, -physics.max_velocity, physics.max_velocity)

            # Update position
            p.x += p.vx * physics.time_step
            p.y += p.vy * physics.time_step

            # Boundary conditions (wrap around)
            p.x %= width
            p.y %= height
            
            total_dx += abs(p.vx)
            total_dy += abs(p.vy)
            center_x += p.x
            center_y += p.y
        
        if org.particles:
            org.mobility = (total_dx + total_dy) / len(org.particles)
            center_x /= len(org.particles)
            center_y /= len(org.particles)

        # --- Metabolism & Survival ---
        metabolic_cost = len(org.particles) * settings['energy_cost_per_particle']
        org.energy -= metabolic_cost
        
        # Energy from environment
        if org.particles:
            int_cx, int_cy = int(center_x), int(center_y)
            if 0 <= int_cx < width and 0 <= int_cy < height:
                consumed_energy = resources[int_cx, int_cy] * settings['resource_uptake_rate']
                org.energy += consumed_energy
                resources[int_cx, int_cy] -= consumed_energy

        # Check for death
        if org.energy <= 0:
            org.is_alive = False

# ==============================================================================
# 4. VISUALIZATION
# ==============================================================================

def visualize_universe(organisms: List[Organism], resources: np.ndarray, settings: Dict):
    """Renders the current state of the universe."""
    width, height = resources.shape
    
    fig = go.Figure()

    # 1. Resources heatmap
    fig.add_trace(go.Heatmap(
        z=resources.T, # Transpose for correct orientation
        colorscale='Greens',
        showscale=False,
        name='Resources'
    ))

    # 2. Organisms
    all_x, all_y, all_colors, all_sizes, all_hover_text = [], [], [], [], []
    bond_x, bond_y = [], []

    for org in organisms:
        if not org.is_alive:
            continue
        
        element_map = {e.id: e for e in settings['chemistry'].elements}

        for p in org.particles.values():
            all_x.append(p.x)
            all_y.append(p.y)
            element = element_map.get(p.element_id)
            if element:
                all_colors.append(element.color)
                all_sizes.append(element.mass * 2)
                all_hover_text.append(f"Organism: {org.genome.lineage_id[:8]}<br>Element: {element.name}<br>Energy: {org.energy:.2f}")
        
        for bond in org.bonds:
            p1 = org.particles.get(bond.p1_id)
            p2 = org.particles.get(bond.p2_id)
            if p1 and p2:
                bond_x.extend([p1.x, p2.x, None])
                bond_y.extend([p1.y, p2.y, None])

    # Add bonds first (background)
    fig.add_trace(go.Scatter(
        x=bond_x, y=bond_y,
        mode='lines',
        line=dict(color='rgba(128, 128, 128, 0.5)', width=2),
        hoverinfo='none',
        name='Bonds'
    ))

    # Add particles on top
    fig.add_trace(go.Scatter(
        x=all_x, y=all_y,
        mode='markers',
        marker=dict(
            color=all_colors,
            size=all_sizes,
            line=dict(width=1, color='black')
        ),
        hovertext=all_hover_text,
        hoverinfo='text',
        name='Organisms'
    ))

    fig.update_layout(
        title=f"Universe Sandbox | Generation: {st.session_state.get('generation', 0)} | Population: {len(organisms)}",
        xaxis=dict(range=[0, width], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, height], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1),
        plot_bgcolor='black',
        height=700,
        showlegend=False
    )
    
    return fig

# ==============================================================================
# 5. STREAMLIT APP UI
# ==============================================================================

def main():
    st.set_page_config(
        page_title="Universe Sandbox AI",
        layout="wide",
        page_icon="🌌"
    )

    st.title("🌌 Universe Sandbox AI")
    st.markdown("An interactive laboratory for abiogenesis and open-ended evolution. Define the laws of physics and chemistry, then watch as life emerges and complexifies from a primordial soup.")

    # --- SIDEBAR: The Control Panel of God ---
    st.sidebar.header("🚀 Universe Configuration")

    # Initialize session state
    if 'settings' not in st.session_state:
        st.session_state.settings = {}
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    if 'organisms' not in st.session_state:
        st.session_state.organisms = []
    if 'generation' not in st.session_state:
        st.session_state.generation = 0

    s = st.session_state.settings

    with st.sidebar.expander("🔬 Fundamental Constants", expanded=True):
        st.markdown("#### Physics")
        gravity = st.slider("Gravity", 0.0, 0.5, s.get('gravity', 0.01), 0.005, key='gravity')
        friction = st.slider("Friction", 0.8, 1.0, s.get('friction', 0.95), 0.01, key='friction')
        
        st.markdown("#### Chemistry")
        # Define a default set of elements
        default_elements = [
            Element(id=0, name='Substrate', color='grey', mass=5, max_bonds=1),
            Element(id=1, name='Carbon', color='blue', mass=10, max_bonds=4, properties={'structural'}),
            Element(id=2, name='Oxygen', color='red', mass=12, max_bonds=2),
            Element(id=3, name='PhotonReceptor', color='yellow', mass=8, max_bonds=3, properties={'photosynthetic'}),
            Element(id=4, name='Silicon', color='purple', mass=14, max_bonds=4, properties={'structural'}),
        ]
        # This is a simplified UI. A full version would let you add/remove elements.
        st.info("Chemistry is pre-defined for this demo: Substrate, Carbon, Oxygen, PhotonReceptor, Silicon.")
        
        # Define default bond strengths
        default_bond_strengths = {
            tuple(sorted((1, 1))): 1.0, # C-C
            tuple(sorted((1, 2))): 0.8, # C-O
            tuple(sorted((1, 3))): 0.7, # C-Photo
            tuple(sorted((4, 4))): 0.9, # Si-Si
            tuple(sorted((4, 2))): 0.85, # Si-O
        }

    with st.sidebar.expander("🌊 Primordial Soup"):
        st.markdown("#### Initial Conditions")
        population_size = st.slider("Initial Population Size", 10, 500, s.get('population_size', 100), 10, key='population_size')
        initial_energy = st.slider("Initial Organism Energy", 50, 500, s.get('initial_energy', 100), 10, key='initial_energy')
        initial_genome_length = st.slider("Initial Genome Length", 1, 20, s.get('initial_genome_length', 5), 1, key='initial_genome_length')
        
        st.markdown("#### Environment Resources")
        world_width = st.slider("World Width", 100, 1000, s.get('world_width', 400), 50, key='world_width')
        world_height = st.slider("World Height", 100, 1000, s.get('world_height', 400), 50, key='world_height')
        resource_density = st.slider("Resource Density", 0.1, 1.0, s.get('resource_density', 0.5), 0.05, key='resource_density')
        resource_regeneration = st.slider("Resource Regeneration Rate", 0.0, 0.1, s.get('resource_regeneration', 0.01), 0.005, key='resource_regeneration')

    with st.sidebar.expander("🧬 Evolutionary Dynamics"):
        st.markdown("#### Selection")
        selection_pressure = st.slider("Selection Pressure", 0.1, 0.9, s.get('selection_pressure', 0.5), 0.05, key='selection_pressure')
        reproduction_energy_threshold = st.slider("Reproduction Energy Threshold", 100, 1000, s.get('reproduction_energy_threshold', 200), 10, key='reproduction_energy_threshold')
        
        st.markdown("#### Mutation")
        mutation_rate_point = st.slider("Mutation Rate (Point)", 0.0, 1.0, s.get('mutation_rate_point', 0.1), 0.01, key='mutation_rate_point')
        mutation_rate_insertion = st.slider("Mutation Rate (Insertion)", 0.0, 1.0, s.get('mutation_rate_insertion', 0.05), 0.01, key='mutation_rate_insertion')
        mutation_rate_deletion = st.slider("Mutation Rate (Deletion)", 0.0, 1.0, s.get('mutation_rate_deletion', 0.05), 0.01, key='mutation_rate_deletion')
        mutation_rate_duplication = st.slider("Mutation Rate (Duplication)", 0.0, 1.0, s.get('mutation_rate_duplication', 0.02), 0.01, key='mutation_rate_duplication')

    with st.sidebar.expander("⚖️ Fitness Objectives"):
        st.markdown("Define what it means to be 'fit' in this universe.")
        w_integrity = st.slider("Weight: Structural Integrity", 0.0, 1.0, s.get('w_integrity', 0.3), 0.05, key='w_integrity')
        w_energy_generation = st.slider("Weight: Energy Generation", 0.0, 1.0, s.get('w_energy_generation', 0.4), 0.05, key='w_energy_generation')
        w_size = st.slider("Weight: Optimal Size", 0.0, 1.0, s.get('w_size', 0.1), 0.05, key='w_size')
        w_mobility = st.slider("Weight: Mobility", 0.0, 1.0, s.get('w_mobility', 0.2), 0.05, key='w_mobility')
        optimal_organism_size = st.slider("Optimal Organism Size (Particles)", 5, 100, s.get('optimal_organism_size', 20), 1, key='optimal_organism_size')

    with st.sidebar.expander("⚡ Metabolic Costs"):
        energy_cost_per_particle = st.slider("Energy Cost per Particle", 0.0, 2.0, s.get('energy_cost_per_particle', 0.5), 0.05, key='energy_cost_per_particle')
        resource_uptake_rate = st.slider("Resource Uptake Rate", 0.1, 1.0, s.get('resource_uptake_rate', 0.5), 0.05, key='resource_uptake_rate')

    # --- Store settings ---
    st.session_state.settings = {
        'physics': PhysicsConstants(gravity=gravity, friction=friction),
        'chemistry': Chemistry(elements=default_elements, bond_strengths=default_bond_strengths),
        'population_size': population_size,
        'initial_energy': initial_energy,
        'initial_genome_length': initial_genome_length,
        'world_width': world_width,
        'world_height': world_height,
        'resource_density': resource_density,
        'resource_regeneration': resource_regeneration,
        'selection_pressure': selection_pressure,
        'reproduction_energy_threshold': reproduction_energy_threshold,
        'mutation_rate_point': mutation_rate_point,
        'mutation_rate_insertion': mutation_rate_insertion,
        'mutation_rate_deletion': mutation_rate_deletion,
        'mutation_rate_duplication': mutation_rate_duplication,
        'w_integrity': w_integrity,
        'w_energy_generation': w_energy_generation,
        'w_size': w_size,
        'w_mobility': w_mobility,
        'optimal_organism_size': optimal_organism_size,
        'energy_cost_per_particle': energy_cost_per_particle,
        'resource_uptake_rate': resource_uptake_rate
    }
    s = st.session_state.settings

    # --- Main Controls ---
    c1, c2, c3 = st.sidebar.columns(3)
    start_button = c1.button("▶️ Start", use_container_width=True)
    stop_button = c2.button("⏹️ Stop", use_container_width=True)
    reset_button = c3.button("Reset", use_container_width=True)

    if start_button:
        st.session_state.simulation_running = True
        if not st.session_state.organisms: # If starting fresh
            st.session_state.generation = 0
            # Initialize resources
            st.session_state.resources = np.random.rand(s['world_width'], s['world_height']) * s['resource_density']
            
            # Initialize population
            organisms = []
            for _ in range(s['population_size']):
                # Create a random genome
                tape = []
                for _ in range(s['initial_genome_length']):
                    tape.append({"cmd": "ADD_PARTICLE", "element_id": random.choice(s['chemistry'].elements).id})
                    tape.append({"cmd": "MOVE", "direction": random.choice(["N", "S", "E", "W"])})
                genome = Genome(tape=tape)
                
                particles, bonds = run_development(genome, s['chemistry'])
                org = Organism(genome=genome, particles=particles, bonds=bonds, energy=s['initial_energy'])
                organisms.append(org)
            st.session_state.organisms = organisms
            st.toast("Universe created! Simulation started.", icon="🌠")

    if stop_button:
        st.session_state.simulation_running = False
        st.toast("Simulation paused.", icon="⏸️")

    if reset_button:
        st.session_state.simulation_running = False
        st.session_state.organisms = []
        st.session_state.generation = 0
        st.toast("Universe reset.", icon="🔄")
        st.rerun()

    # --- Main Simulation Display ---
    placeholder = st.empty()

    if not st.session_state.simulation_running and not st.session_state.organisms:
        placeholder.info("Configure your universe in the sidebar and press 'Start' to begin abiogenesis.")

    while st.session_state.simulation_running:
        organisms = st.session_state.organisms
        resources = st.session_state.resources
        
        # --- Main Loop ---
        update_world(organisms, resources, s['physics'], s['chemistry'], s)
        
        # --- Reproduction and Selection ---
        new_offspring = []
        survivors = []
        
        for org in organisms:
            if org.is_alive:
                org.fitness = evaluate_fitness(org, s['chemistry'], s)
                survivors.append(org)
        
        if not survivors:
            st.session_state.simulation_running = False
            st.error("EXTINCTION EVENT! All life has perished.")
            break

        survivors.sort(key=lambda o: o.fitness, reverse=True)
        
        num_to_reproduce = int(len(survivors) * s['selection_pressure'])
        parents = survivors[:num_to_reproduce]

        for parent in parents:
            if parent.energy > s['reproduction_energy_threshold']:
                parent.energy /= 2 # Cost of reproduction
                child_genome = mutate_genome(parent.genome, s['chemistry'], s)
                child_genome.generation = st.session_state.generation + 1
                
                particles, bonds = run_development(child_genome, s['chemistry'])
                if particles: # Only add viable offspring
                    child = Organism(genome=child_genome, particles=particles, bonds=bonds, energy=parent.energy)
                    new_offspring.append(child)

        st.session_state.organisms = survivors + new_offspring
        st.session_state.generation += 1

        # Regenerate resources
        st.session_state.resources += s['resource_regeneration']
        st.session_state.resources = np.clip(st.session_state.resources, 0, 1.0)

        # --- Visualization ---
        with placeholder.container():
            fig = visualize_universe(st.session_state.organisms, st.session_state.resources, s)
            st.plotly_chart(fig, use_container_width=True)
            
            # Stats
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Generation", st.session_state.generation)
            c2.metric("Population", len(st.session_state.organisms))
            c3.metric("Mean Fitness", f"{np.mean([o.fitness for o in survivors]):.4f}" if survivors else "N/A")
            c4.metric("Max Fitness", f"{survivors[0].fitness:.4f}" if survivors else "N/A")

        time.sleep(0.1) # Control simulation speed

if __name__ == "__main__":
    main()
