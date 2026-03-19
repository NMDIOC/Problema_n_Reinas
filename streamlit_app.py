import streamlit as st
import time
import json
import base64
import os

# --- Algoritmo Optimizado ---
def resolver_n_reinas(n):
    soluciones = []
    tablero = [["." for _ in range(n)] for _ in range(n)]
    cols, d_pos, d_neg = set(), set(), set()

    def backtrack(fila):
        if fila == n:
            soluciones.append([" ".join(r) for r in tablero])
            return
        for col in range(n):
            if col in cols or (fila+col) in d_pos or (fila-col) in d_neg:
                continue
            cols.add(col); d_pos.add(fila+col); d_neg.add(fila-col)
            tablero[fila][col] = "Q"
            backtrack(fila + 1)
            tablero[fila][col] = "."
            cols.remove(col); d_pos.remove(fila+col); d_neg.remove(fila-col)

    backtrack(0)
    return soluciones

# --- Función de Auto-Descarga Mejorada ---
def trigger_auto_download(data_dict, filename):
    json_str = json.dumps(data_dict, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    
    # Este JS crea un link invisible y lo pulsa automáticamente
    # Usamos un ID único para evitar conflictos
    download_script = f"""
        <script>
            function download() {{
                var a = document.createElement("a");
                a.href = "data:application/json;base64,{b64}";
                a.download = "{filename}";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }}
            // Ejecutar después de un breve delay para asegurar que el DOM cargó
            setTimeout(download, 500);
        </script>

    st.markdown(download_script, unsafe_allow_html=True)

# --- Interfaz Principal ---
def main():
    st.set_page_config(page_title="N-Queens Deep Solver", layout="wide")
    st.title("⚙️ N-Queens: Procesador Nocturno")
    
    n = st.number_input("Valor de N:", min_value=1, max_value=16, value=12)
    
    if st.button("🚀 Iniciar Cálculo"):
        status = st.empty()
        status.info(f"Procesando N={n}... Al terminar se guardará en tu PC.")
        
        inicio = time.perf_counter()
        resultados = resolver_n_reinas(n)
        fin = time.perf_counter()
        
        tiempo_total = fin - inicio
        nombre_archivo = f"reinas_N{n}_resultado.json"
        
        datos = {
            "configuracion_n": n,
            "total_soluciones": len(resultados),
            "tiempo_segundos": tiempo_total,
            "soluciones": resultados
        }

        # --- SEGURIDAD 1: Guardado en el Disco Duro (Carpeta del script) ---
        with open(nombre_archivo, "w") as f:
            json.dump(datos, f, indent=4)
        
        # --- SEGURIDAD 2: Intento de descarga automática en navegador ---
        trigger_auto_download(datos, nombre_archivo)
        
        # Reporte final en pantalla
        status.success(f"✅ Proceso terminado en {tiempo_total:.2f} segundos.")
        
        col1, col2 = st.columns(2)
        col1.metric("Soluciones", len(resultados))
        col1.write(f"📂 **Archivo guardado en carpeta:** `{os.path.abspath(nombre_archivo)}`")
        
        if resultados:
            col2.subheader("Muestra de la primera solución:")
            col2.code("\n".join(resultados[0]), language="text")
        
        st.balloons()

if __name__ == "__main__":
    main()
