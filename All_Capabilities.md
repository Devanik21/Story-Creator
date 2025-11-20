# 🧬 Organism Action Registry

Below is the complete list of actions (functions) available to organisms within the Universe Sandbox 2.0 simulation. These actions are triggered by the organism's Genetic Regulatory Network (GRN) based on environmental sensors and internal logic.

## 🌱 Core Development & Growth
These actions control the physical growth and life cycle of the organism.

| Action | Description |
| :--- | :--- |
| **`GROW`** | Creates a new cell in an adjacent empty grid space using a specific component type. |
| **`DIFFERENTIATE`** | Transforms an existing cell into a different component type (e.g., turning a *Stem* into a *Brain*). |
| **`DIE`** | The cell commits programmed suicide (apoptosis), removing itself from the grid. |
| **`SPLIT`** | **Binary Fission:** Detaches the cell from the main body to form a completely new, independent organism ID. |
| **`REPRODUCE`** | **Cloning:** Creates a genetic clone (child zygote) in an adjacent empty space. |

## 🧠 Computation & Logic (The "Brain")
These actions allow the organism to "think," remember, and regulate its own genes.

| Action | Description |
| :--- | :--- |
| **`ENABLE_RULE`** | Turns **ON** a specific gene/rule in the genome (Genetic Switch). |
| **`DISABLE_RULE`** | Turns **OFF** a specific gene/rule in the genome. |
| **`SET_STATE`** | Sets an internal memory variable within the cell. |
| **`SET_TIMER`** | Starts an internal countdown clock (allows for sequential development). |
| **`MODIFY_TIMER`** | Adds or subtracts time from an active timer. |

## 📡 Communication & Networking
These actions allow cells to coordinate with each other or form hive minds.

| Action | Description |
| :--- | :--- |
| **`EMIT_SIGNAL`** | Releases a chemical signal to neighbors (Morphogenesis/Signaling). |
| **`NETWORK`** | Connects the cell to the organism's global "Mycelial Network" to share pooled energy. |
| **`TRANSFER_ENERGY`** | Donates energy to a specific neighbor (Altruism). |
| **`SYMBIOTE`** | Bonds with a neighbor of a *different* species to form a symbiotic relationship. |

## ⚔️ Combat & Predation
These actions are used for offense, defense, and hunting.

| Action | Description |
| :--- | :--- |
| **`ATTACK`** | Deals physical damage to a neighbor based on the `offense` stat. |
| **`STEAL`** | Parasitically drains energy from a neighbor. |
| **`POISON`** | Releases toxins that damage **all** surrounding neighbors (Area of Effect). |
| **`ABSORB`** | **Engulfment:** Instantly kills and digests a smaller/weaker neighbor (The Blob attack). |
| **`DETONATE`** | **Self-Destruct:** The cell explodes, dealing massive damage to all neighbors. |
| **`RADIATE`** | Emits damaging radiation that hurts neighbors and depletes local minerals. |

## 🛡️ Defense & Survival
These actions help the organism survive harsh environments or attacks.

| Action | Description |
| :--- | :--- |
| **`FORTIFY`** | Temporarily boosts armor/defense for one tick. |
| **`CAMOUFLAGE`** | Makes the cell invisible to `ATTACK` actions for a set duration. |
| **`HIBERNATE`** | Enters a low-energy stasis sleep for a set duration. |
| **`SPORE`** | Transforms into a dormant, heavily armored spore that can survive almost anything. |
| **`REGENERATE`** | Rapidly converts local minerals into health/energy. |
| **`MUTATE_SELF`** | **Epigenetics:** Randomly boosts one of the cell's own stats (Armor/Offense) in real-time. |

## 🌍 Environmental Interaction
These actions allow the organism to move through or alter the physical world.

| Action | Description |
| :--- | :--- |
| **`MOVE`** | Uses `motility` to jump to an adjacent empty grid space. |
| **`MINE_RESOURCE`** | Permanently extracts minerals from the grid tile. |
| **`HARVEST_CORPSE`** | Consumes minerals from the tile as if they were biomass (scavenging). |
| **`TERRAFORM`** | Actively heats up or cools down the local temperature. |
| **`EMIT_LIGHT`** | **Bioluminescence:** Converts energy into light, illuminating the area for neighbors. |
| **`ADAPT`** | Adjusts the cell's internal temperature preference to match the local environment. |
