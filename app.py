import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# ==============================================================================
# CLASE POO: DataAnalyzer (ENCAPSULAMIENTO DE LÓGICA Y VISUALIZACIÓN)
# ==============================================================================
class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def clasificar_variables(self):
        """Ítem 2: Clasificación de variables numéricas y categóricas"""
        numericas = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categoricas = self.df.select_dtypes(include=["object", "category"]).columns.tolist()
        return numericas, categoricas

    def estadisticas_descriptivas(self):
        """Ítem 3: Estadísticas con media, mediana, moda y dispersión"""
        desc = self.df.describe().T
        desc["mediana"] = self.df.median(numeric_only=True)
        # Cálculo de moda para cada columna numérica
        modas = [self.df[col].mode().iloc[0] if not self.df[col].mode().empty else np.nan for col in desc.index]
        desc["moda"] = modas
        return desc[["mean", "mediana", "moda", "std", "min", "25%", "50%", "75%", "max"]]

    def analisis_nulos(self):
        """Ítem 4: Conteo y porcentaje de valores faltantes"""
        conteo = self.df.isnull().sum()
        pct = (conteo / len(self.df)) * 100
        tabla_nulos = pd.DataFrame({"Valores Nulos": conteo, "Porcentaje (%)": pct})
        return tabla_nulos[tabla_nulos["Valores Nulos"] > 0]

    def graficar_distribucion_numerica(self, columna, bins=30, mostrar_kde=True):
        """Ítem 5: Histograma con control de bins y KDE"""
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(self.df[columna].dropna(), bins=bins, kde=mostrar_kde, ax=ax, color="#1f77b4")
        ax.set_title(f"Distribución de: {columna}", fontsize=12, fontweight="bold")
        ax.set_xlabel(columna)
        ax.set_ylabel("Frecuencia")
        return fig

    def graficar_categorica(self, columna):
        """Ítem 6: Conteo de frecuencias para categóricas"""
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(data=self.df, x=columna, ax=ax, palette="Set2")
        ax.set_title(f"Frecuencia por: {columna}", fontsize=12, fontweight="bold")
        ax.set_xlabel(columna)
        ax.set_ylabel("Cantidad")
        return fig

    def graficar_num_vs_cat(self, col_num, col_cat="renewal"):
        """Ítem 7: Comparación bivariada (Boxplot)"""
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=self.df, x=col_cat, y=col_num, ax=ax, palette="pastel")
        ax.set_title(f"Comparación: {col_num} según {col_cat}", fontsize=12, fontweight="bold")
        return fig

    def graficar_cat_vs_cat(self, col_cat1, col_cat2="renewal"):
        """Ítem 8: Bivariado categórico (Barras 100% apiladas)"""
        tabla = pd.crosstab(self.df[col_cat1], self.df[col_cat2], normalize="index") * 100
        fig, ax = plt.subplots(figsize=(8, 4))
        tabla.plot(kind="bar", stacked=True, ax=ax, colormap="coolwarm")
        ax.set_title(f"Proporción de {col_cat2} según {col_cat1} (%)", fontsize=12, fontweight="bold")
        ax.set_ylabel("Porcentaje (%)")
        ax.legend(title=col_cat2, loc="upper right")
        return fig

st.title(" Proyecto Final de Python DMC")
st.sidebar.title("Módulos")

st.image("Python_logo.png")
st.sidebar.image("DMC.png")

modulos = st.sidebar.selectbox("Elija un módulo", ["Home","Carga del Dataset","Análisis Exploratorio de Datos (EDA)"])

if modulos == "Home":
 st.subheader("Módulo 2 - Pyhon Data Analytics")
 st.subheader("Alumno: Richard Antonio Chincha Ugarte")
 st.markdown("-----")
 st.write("Alumno de la especialización en Python for Analytics")
 st.write("Año: 2026")
 st.write("Dataset sobre la base de clientes de una empresa de seguros")
 st.write("Tecnologías: Uso de Pandas, numpy, streamlit")

 elif hojas =="Carga del Dataset":
    st.subheader("Carga del dataset Insurance Company")
    st.markdown("-----")
    
    archivo = st.file_uploader("Cargue el archivo CSV", type=["csv"])
    
    if archivo is not None:
        try:
            # Lectura y guardado directo en st.session_state
            st.session_state["df"] = pd.read_csv(archivo)
            st.success("Archivo cargado y validado con éxito.")
            
            # Dimensiones del dataset
            filas, columnas = st.session_state["df"].shape
            col1, col2 = st.columns(2)
            col1.metric("Total de Filas", f"{filas:,}")
            col2.metric("Total de Columnas", f"{columnas}")
            
            # Vista previa
            st.subheader("Vista previa del dataset (Primeras 5 filas)")
            st.dataframe(st.session_state["df"].head(), use_container_width=True)
            
        except Exception as e:
            st.error(f" Error al procesar el archivo CSV: {e}")
            st.session_state["df"] = None
    else:
        # Si no se sube uno nuevo pero ya existía uno cargado
        if "df" in st.session_state and st.session_state["df"] is not None:
            st.info(" Dataset previamente cargado y activo en memoria.")
            st.dataframe(st.session_state["df"].head(), use_container_width=True)
        else:
            st.warning(" Debe subir el archivo .csv para continuar.")
          
 elif hojas =="Análisis Exploratorio de Datos (EDA)":   
    st.subheader(" Módulo 2: Análisis Exploratorio de Datos (EDA)")
    st.markdown("---")
    
    # Validación obligatoria: bloqueo si no se cargó el archivo
    if "df" not in st.session_state or st.session_state["df"] is None:
        st.error(" Acceso bloqueado: Primero debe cargar el dataset en el **Módulo 1**.")
    else:
        df = st.session_state["df"]
        
        # Instanciación de la clase POO
        analyzer = DataAnalyzer(df)
        num_cols, cat_cols = analyzer.clasificar_variables()
    
        # Widget obligatorio: st.tabs para organizar los 10 ítems
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Estructura & Tipos (Ítems 1-2)",
            "Estadísticas & Nulos (Ítems 3-4)",
            "Distribuciones & Conteos (Ítems 5-6)",
            "Análisis Bivariado (Ítems 7-8)",
            "Parámetros & Hallazgos (Ítems 9-10)"
        ])
    
        # --------------------------------------------------------------------------
        # TAB 1: ÍTEMS 1 Y 2
        # --------------------------------------------------------------------------
        with tab1:
            st.markdown(" Ítem 1: Información General del Dataset")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Estructura y Resumen `.info()`:**")
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())
            with col2:
                st.write("**Conteo de Nulos y Tipos por Columna:**")
                info_resumen = df.dtypes.to_frame(name="Tipo de Dato")
                info_resumen["Nulos"] = df.isnull().sum()
                info_resumen["% Nulos"] = ((df.isnull().sum() / len(df)) * 100).round(2)
                st.dataframe(info_resumen, use_container_width=True)
    
            st.markdown("---")
            st.markdown(" Ítem 2: Clasificación de Variables (Función POO)")
            col3, col4 = st.columns(2)
            with col3:
                st.info(f" **Variables Numéricas ({len(num_cols)} identificadas):**")
                st.write(num_cols)
            with col4:
                st.success(f" **Variables Categóricas ({len(cat_cols)} identificadas):**")
                st.write(cat_cols)
    
        # --------------------------------------------------------------------------
        # TAB 2: ÍTEMS 3 Y 4
        # --------------------------------------------------------------------------
        with tab2:
            st.markdown(" Ítem 3: Estadísticas Descriptivas")
            st.write("Medidas de tendencia central (**media, mediana, moda**) y dispersión (**desviación estándar, cuartiles**):")
            st.dataframe(analyzer.estadisticas_descriptivas(), use_container_width=True)
    
            st.markdown("---")
            st.markdown("Ítem 4: Análisis y Discusión de Valores Faltantes")
            df_nulos = analyzer.analisis_nulos()
            if not df_nulos.empty:
                col_n1, col_n2 = st.columns([1, 1])
                with col_n1:
                    st.dataframe(df_nulos, use_container_width=True)
                with col_n2:
                    fig_n, ax_n = plt.subplots(figsize=(7, 3.5))
                    df_nulos["Porcentaje (%)"].plot(kind="barh", ax=ax_n, color="#e74c3c")
                    ax_n.set_title("% de Valores Faltantes por Columna", fontweight="bold")
                    ax_n.set_xlabel("% Faltante")
                    st.pyplot(fig_n)
                st.info(" **Discusión:** Variables como `application_underwriting_score` y los conteos de morosidad presentan valores nulos que requerirán imputación o tratamiento antes de modelar.")
            else:
                st.success(" El dataset no registra valores faltantes.")
    
        # --------------------------------------------------------------------------
        # TAB 3: ÍTEMS 5 Y 6
        # --------------------------------------------------------------------------
        with tab3:
            st.markdown(" Ítem 5: Distribución de Variables Numéricas")
            col_ctrl1, col_ctrl2 = st.columns(2)
            with col_ctrl1:
                # Widgets obligatorios: st.selectbox, st.slider, st.checkbox
                col_num_sel = st.selectbox("Seleccione la variable numérica a analizar:", num_cols, index=3)
            with col_ctrl2:
                bins_sel = st.slider("Ajustar número de intervalos (Bins):", min_value=10, max_value=100, value=30, step=5)
                kde_activo = st.checkbox("Mostrar curva de densidad (KDE)", value=True)
                
            st.pyplot(analyzer.graficar_distribucion_numerica(col_num_sel, bins=bins_sel, mostrar_kde=kde_activo))
    
            st.markdown("---")
            st.markdown(" Ítem 6: Análisis de Variables Categóricas")
            col_cat_sel = st.selectbox("Seleccione la variable categórica:", cat_cols, index=0)
            
            col_c1, col_c2 = st.columns([1, 1])
            with col_c1:
                st.write("**Tabla de Frecuencias y Proporciones:**")
                tabla_cat = df[col_cat_sel].value_counts().to_frame(name="Conteo")
                tabla_cat["Proporción (%)"] = (df[col_cat_sel].value_counts(normalize=True) * 100).round(2)
                st.dataframe(tabla_cat, use_container_width=True)
            with col_c2:
                st.pyplot(analyzer.graficar_categorica(col_cat_sel))
    
        # --------------------------------------------------------------------------
        # TAB 4: ÍTEMS 7 Y 8
        # --------------------------------------------------------------------------
        with tab4:
            st.markdown(" Ítem 7: Análisis Bivariado (Numérico vs Categórico / Renewal)")
            col_biv_num = st.selectbox(
                "Seleccione la variable numérica a contrastar con Renewal:",
                [c for c in num_cols if c not in ["id", "renewal"]],
                index=1
            )
            st.pyplot(analyzer.graficar_num_vs_cat(col_biv_num, col_cat="renewal"))
    
            st.markdown("---")
            st.markdown(" Ítem 8: Análisis Bivariado (Categórico vs Categórico)")
            col_biv_cat = st.selectbox(
                "Seleccione la variable categórica a contrastar con Renewal:",
                cat_cols,
                index=0
            )
            st.pyplot(analyzer.graficar_cat_vs_cat(col_biv_cat, col_cat2="renewal"))
    
        # --------------------------------------------------------------------------
        # TAB 5: ÍTEMS 9 Y 10
        # --------------------------------------------------------------------------
        with tab5:
            st.markdown(" Ítem 9: Análisis Basado en Parámetros Dinámicos")
            # Widget obligatorio: st.multiselect
            cols_corr = st.multiselect(
                "Seleccione las variables para la Matriz de Correlación:",
                num_cols,
                default=["Income", "premium", "renewal", "no_of_premiums_paid", "perc_premium_paid_by_cash_credit"]
            )
            ver_anotaciones = st.checkbox("Mostrar valores numéricos en el mapa de calor", value=True)
            
            if len(cols_corr) > 1:
                fig_corr, ax_corr = plt.subplots(figsize=(8, 4))
                sns.heatmap(df[cols_corr].corr(), annot=ver_anotaciones, cmap="coolwarm", fmt=".2f", ax=ax_corr)
                st.pyplot(fig_corr)
            else:
                st.warning(" Seleccione al menos dos columnas para generar el mapa de correlación.")
    
            st.markdown("---")
            st.markdown(" Ítem 10: Hallazgos Clave & Insights del EDA")
            
            kpi1, kpi2, kpi3 = st.columns(3)
            tasa_renovacion = (df["renewal"].mean()) * 100
            ingreso_promedio = df["Income"].mean()
            prima_promedio = df["premium"].mean()
    
            kpi1.metric("Tasa de Renovación", f"{tasa_renovacion:.2f}%")
            kpi2.metric("Ingreso Promedio", f"${ingreso_promedio:,.0f}")
            kpi3.metric("Prima Promedio", f"${prima_promedio:,.0f}")
    
            st.markdown(
                """
                > **Hallazgos Principales:**
                > * **Morosidad:** Los clientes con pagos atrasados (`Count_3-6_months_late`) presentan una probabilidad de renovación drásticamente menor.
                > * **Modalidad de Pago:** Un alto porcentaje de prima pagada por efectivo/crédito (`perc_premium_paid_by_cash_credit`) se asocia a mayor riesgo de no renovación.
                > * **Canales de Captación:** El canal `sourcing_channel` influye en la tasa de retención, mostrando oportunidades claras de fidelización segmentada.
                """
            )
    
    
