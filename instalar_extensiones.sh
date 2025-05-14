#!/bin/bash

echo "📦 Instalando extensiones para VSCodium..."

# Verifica si codium está instalado
if ! command -v codium &> /dev/null; then
    echo "❌ VSCodium no está instalado. Abortando."
    exit 1
fi

# Lista de extensiones a instalar
EXTENSIONS=(
  ms-python.python                 # Soporte para Python
  ms-python.vscode-pylance        # Autocompletado avanzado con Pylance
  formulahendry.code-runner       # Ejecutar código fácilmente
  tkhoa.vscode-tkinter-snippets   # Fragmentos para Tkinter
  eamodio.gitlens                 # Git avanzado
  github.vscode-pull-request-github  # GitHub integración
  mtxr.sqltools                    # Cliente de base de datos
  mtxr.sqltools-driver-mysql      # Driver para MySQL
  alexcvzz.vscode-sqlite          # Ver bases SQLite
  TabNine.tabnine-vscode          # Autocompletado con IA
)

for EXT in "${EXTENSIONS[@]}"
do
  echo "🔧 Instalando: $EXT"
  codium --install-extension "$EXT"
done

echo "✅ Todo listo. Reiniciá VSCodium si estaba abierto."
