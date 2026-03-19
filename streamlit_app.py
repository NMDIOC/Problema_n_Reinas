import streamlit as st
import time
import json

# --- Lógica del Algoritmo (Backtracking) ---
def resolver_n_reinas(n):
    soluciones = []
    tablero = [["." for _ in range(n)] for _ in range(n)]
    columnas_ocupadas, diag_pos, diag_neg = set(), set(), set()

    def backtrack(fila):
        if fila == n:
            soluciones.append([" ".join(r) for r in tablero])
            return
        for col in range(n):
            if col in columnas_ocupadas or (fila+col) in diag_pos or (fila-col) in diag_neg:
                continue
            columnas_ocupadas.add(col); diag_pos.add(fila+col); diag_neg.add(fila-col)
            tablero[fila][col] = "Q"
            backtrack(fila + 1)
            tablero[fila][col] = "."
            columnas_ocupadas.remove(col); diag_pos.remove(fila+col); diag_neg.remove(fila-col)

    backtrack(0)
    return soluciones

# --- Interfaz de Streamlit ---
def main():
    st.title("N-Queens Solver & Downloader")
    n = st.number_input("Valor de N:", min_value=1, max_value=15, value=8)

    if st.button("Ejecutar"):
        with st.spinner(f"Calculando soluciones para N={n}..."):
            inicio = time.perf_counter()
            resultados = resolver_n_reinas(n)
            fin = time.perf_counter()
            
        tiempo = fin - inicio
        
        # 1. Mostrar resultados en pantalla
        st.success(f"¡Hecho! {len(resultados)} soluciones en {tiempo:.4f}s")

        # 2. Preparar los datos para descarga (JSON)
        datos_json = json.dumps({
            "N": n,
            "total_soluciones": len(resultados),
            "tiempo_segundos": tiempo,
            "todas_las_soluciones": resultados
        }, indent=4)

        # 3. BOTÓN DE DESCARGA (Esto es lo que faltaba)
        st.download_button(
            label="📥 Descargar resultados (.json)",
            data=datos_json,
            file_name=f"reinas_N{n}.json",
            mime="application/json"
        )

        # Visualización rápida de la primera
        if resultados:
            st.subheader("Primera solución encontrada:")
            st.code("\n".join(resultados[0]), language="text")

if __name__ == "__main__":
    main()
