import re

# Ouvrir le fichier texte et le lire
with open("seeds/stable.txt", "r") as f:
    file_content = f.read()

# Trouver la valeur de x
x = int(re.search(r"x\s*=\s*(\d+)", file_content).group(1))

# Trouver la valeur de y
y = int(re.search(r"y\s*=\s*(\d+)", file_content).group(1))

# Trouver les coordonnées de seed
seed_str = re.search(r"seed\s*=\s*(.+)", file_content).group(1)
seed = set((int(x), int(y)) for (x, y) in re.findall(r"\((\d+),\s*(\d+)\)", seed_str))

for s in seed:
	print(s[0])

print(x)
print(y)
print(seed)