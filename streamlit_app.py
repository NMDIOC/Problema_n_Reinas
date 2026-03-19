import streamlit as st
import time
import json
import os

# --- Lógica del Algoritmo ---
def resolver_n_reinas(n):
    soluciones = []
    tablero = [["." for _ in range(n)] for _ in range(n)]

    columnas_ocupadas = set()
    diagonales_positivas = set()
    diagonales_negativas = set()

    def backtrack(fila):
        if fila == n:
            copia_solucion = [" ".join(fila_actual) for fila_actual in tablero]
            soluciones.append(copia_solucion)
            return

        for col in range(n):
            if (col in columnas_ocupadas or 
                (fila + col) in diagonales_positivas or 
                (fila - col) in diagonales_negativas):
                continue

            columnas_ocupadas.add(col)
            diagonales_positivas.add(fila + col)
            diagonales_negativas.add(fila - col)
            tablero[fila][col] = "Q"

            backtrack(fila + 1)

            columnas_ocupadas.remove(col)
            diagonales_positivas.remove(fila + col)
            diagonales_negativas.remove(fila - col)
            tablero[fila][col] = "."

    backtrack(0)
    return soluciones

# --- Sistema de Guardado ---
def guardar_resultados(n, tiempo, soluciones):
    archivo_salida = f"resultados_reinas_N{n}.json"
    datos = {
        "N": n,
        "tiempo_ejecucion_segundos": tiempo,
        "total_soluciones": len(soluciones),
        "primera_solucion": soluciones[0] if soluciones else []
    }
    
    with open(archivo_salida, "w") as f:
        json.dump(datos, f, indent=4)
    
    return archivo_salida

# --- Interfaz de Streamlit ---
def main():
    st.set_page_config(page_title="Problema de las N Reinas", layout="centered")
    st.title("Calculadora: El Problema de las N Reinas")
    st.markdown("Algoritmo de Backtracking optimizado con verificación de amenazas en $O(1)$.")

    # Entrada de datos
    n = st.number_input("Introduce el valor de N:", min_value=1, max_value=20, value=8, step=1)
    
    # Botón de ejecución
    if st.button("Iniciar Cálculo"):
        st.info(f"Calculando soluciones para N={n}. Por favor, no cierres esta pestaña hasta que termine el proceso.")
        
        # Barra de progreso visual (indeterminada para procesos largos)
        with st.spinner("Procesando algoritmo..."):
            inicio = time.perf_counter()
            resultados = resolver_n_reinas(n)
            fin = time.perf_counter()
        
        tiempo_total = fin - inicio
        total_soluciones = len(resultados)

        # Guardado automático en disco
        ruta_archivo = guardar_resultados(n, tiempo_total, resultados)

        # Despliegue de resultados en la UI
        st.success("¡Cálculo finalizado y guardado exitosamente!")
        
        col1, col2 = st.columns(2)
        col1.metric("Soluciones Encontradas", total_soluciones)
        col2.metric("Tiempo de Ejecución", f"{tiempo_total:.4f} s")

        st.markdown(f"**Archivo de respaldo creado:** `{ruta_archivo}`")

        # Visualización de la primera solución
        if total_soluciones > 0:
            st.subheader("Visualización de la Primera Solución")
            
            # Construcción de la matriz visual
            matriz_texto = ""
            matriz_texto += "   " + " ".join([str(i) for i in range(n)]) + "\n"
            matriz_texto += "   " + "--" * n + "\n"
            for i, fila in enumerate(resultados[0]):
                matriz_texto += f"{i} | {fila}\n"
            matriz_texto += "   " + "--" * n
            
            st.code(matriz_texto, language="text")
            st.caption("'Q' representa la Reina, '.' representa una casilla vacía.")
        elif n > 3 or n == 1:
            st.warning("El algoritmo finalizó, pero no existen soluciones para este tablero.")
        else:
            st.error(f"Matemáticamente, no existen soluciones para N={n}.")

if __name__ == "__main__":
    main()
