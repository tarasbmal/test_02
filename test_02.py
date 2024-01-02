import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def main():
    page = st.sidebar.selectbox("Выбрать страницу", ["Тяжелые хвосты распределений", "Iris Dataset"])

    if page == "Тяжелые хвосты распределений":
        st.header("""Сгенерировать N случайных событий из распределения Фреше с функцией распределения:""")
        st.latex(r'''    
            F(x) = exp(-(\gamma x)^{-1/\gamma}1\{x>0\})
            ''')
        st.text("Для получения результата:")
        st.markdown("* Сгенерируем N нормально распределенных случайных величин $U_i$ [0,1] (нулевое среднее и единичная диспресия).")
        st.markdown("* Вычислим N cлучайных величин с распределением Фреше по формуле:")
        st.latex(r'''    
                    X_i=\dfrac{1}{\gamma}\left(-lnU_i)^{-\gamma}\right)
                ''')
        mu, sigma = 0, 1  # mean and standard deviation
        gamma = st.slider('Желаемая гамма', 0.25, 2.25, 0.5, 0.25)
        N = st.number_input("Желаемое N", 100, 10000, 10000)
        U = np.abs(np.random.normal(mu, sigma, N))
        X = 1 / gamma * (-np.log(U)) ** (-gamma)
        X2 = X[X < 20]
        fig, ax = plt.subplots()
        count, bins, ignored = plt.hist(X2, 100, density=True)
        plt.plot(bins,
                 np.exp(- (gamma * bins) ** (-1 / gamma)) * (1 / gamma) * (gamma * bins) ** (-1 / gamma - 1) * gamma,
                 linewidth=2, color='r')
        st.pyplot(fig)
#---------
main()
