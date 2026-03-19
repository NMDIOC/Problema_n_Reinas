import streamlit as st
import streamlit.components.v1 as components
import time
import json
import base64

# --- Algoritmo N-Reinas ---
def resolver_n_reinas(n):
    soluciones = []
    tablero = [["." for _ in range(n)] for _ in range(n)]
    columnas, diag_pos, diag_neg = set(), set(), set()

    def backtrack(fila):
        if fila == n:
            soluciones.append([" ".join(r) for r in tablero])
            return
        for col in range(n):
            if col in columnas or (fila+col) in diag_pos or (fila-col) in diag_neg:
                continue
            columnas.add(col); diag_pos.add(fila+col); diag_neg.add(fila-col)
            tablero[fila][col] = "Q"
            backtrack(fila + 1)
            tablero[fila][col] = "."
            columnas.remove(col); diag_pos.remove(fila+col); diag_neg.remove(fila-col)

    backtrack(0)
    return soluciones

# --- Función para disparar la descarga automática (JavaScript) ---
def auto_download_js(json_string, file_name):
    # Codificamos el JSON en base64 para pasarlo de forma segura a JavaScript
    b64 = base64.b64encode(json_string.encode()).decode()
    js_code = f"""
        <script>
            var a = document.createElement("a");
            a.href = "data:application/json;base64,{b64}";
            a.download = "{file_name}";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        </script>
    
     # Inyectamos el componente HTML/JS de forma invisible
    components.html(js_code, height=0, width=0)

 --- Interfaz Streamlit ---
def main():
    st.set_page_config(page_title="N-Queens Auto-Downloader", layout="centered")
    st.title("Calculadora N-Reinas con Auto-Descarga")
    st.write("El archivo se descargará automáticamente al terminar el proceso.")

    n = st.number_input("Valor de N:", min_value=1, max_value=15, value=12)

    if st.button("Iniciar Proceso"):
        status_text = st.empty()
        status_text.info(f"🚀 Ejecutando N={n}... Mantén la pestaña activa.")
        
        inicio = time.perf_counter()
        resultados = resolver_n_reinas(n)
        fin = time.perf_counter()
        
        tiempo = fin - inicio
        
        # Preparar datos JSON
        datos = {
            "n": n,
            "total_soluciones": len(resultados),
            "tiempo_segundos": tiempo,
            "soluciones": resultados
        }
        json_string = json.dumps(datos, indent=4)
        
        # Ejecutar la descarga automática
        nombre_archivo = f"resultado_reinas_N{n}.json"
        auto_download_js(json_string, nombre_archivo)
        
        status_text.success(f"✅ ¡Completado! El archivo '{nombre_archivo}' debería haberse descargado.")
        st.balloons()
        
        # Resumen en pantalla
        st.metric("Soluciones", len(resultados))
        st.metric("Tiempo", f"{tiempo:.4f}s")

if __name__ == "__main__":
    main()
