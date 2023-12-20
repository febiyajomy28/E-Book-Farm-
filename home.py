import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
from datetime import datetime
# import altair_viewer


url = "https://raw.githubusercontent.com/Plagrim-Apichaya/830_f23_midterm/main/TH_agri_price.csv"

#####--------------- RICE ---------------####
rice_area = pd.read_csv("https://raw.githubusercontent.com/Plagrim-Apichaya/830_f23_midterm/main/rice.csv",
                        thousands=',')

df = pd.read_csv(url, index_col=0)
def search_content(query, content_list):
    results = []
    for content in content_list:
        if query.lower() in content.lower():
            results.append(content)
    return results

def main():
    
    if 'validasi' not in st.session_state:
        st.session_state.validasi = False
    if 'username' not in st.session_state:
        st.session_state.username = False

    descriptive = df.describe()

    cassava = pd.DataFrame(df.iloc[:,:3])
    corn = pd.DataFrame(df.iloc[:,[0,1,3]])
    rice = pd.DataFrame(df.iloc[:,[0,1,4]])

    select_rice_area = rice_area[rice_area["year"] >= 2014]
    selected_rice_area = select_rice_area[select_rice_area["year"] <= 2019]
    selected_rice_area = selected_rice_area.reset_index()

    rice_mean = rice.groupby('year')['rice_price'].mean().reset_index()
    rice_mean["Rice Area (1000 Ha)"] = selected_rice_area["Area (1000Ha)"]
    rice_mean["Rice Production (1000 Tons)"] = selected_rice_area["Production (1000 Tons)"]
    rice_mean["Rice Yield (T/Ha)"] = selected_rice_area["Yield (T/Ha)"]

    #####--------------- CORN ---------------####
    corn_area = pd.read_csv("https://raw.githubusercontent.com/Plagrim-Apichaya/830_f23_midterm/main/corn.csv",
                        thousands=',')
    select_corn_area = corn_area[corn_area["year"] >= 2014]
    selected_corn_area = select_corn_area[select_corn_area["year"] <= 2019]
    selected_corn_area = selected_corn_area.reset_index()
    corn_mean = corn.groupby('year')['corn_price'].mean().reset_index()
    corn_mean["Corn Area (1000 Ha)"] = selected_corn_area["Area (1000Ha)"]
    corn_mean["Corn Production (1000 Tons)"] = selected_corn_area["Production (1000 Tons)"]
    corn_mean["Corn Yield (T/Ha)"] = selected_corn_area["Yield (T/Ha)"]

    #####--------------- CASSAVA ---------------####
    cassava_mean = cassava.groupby('year')['cassava_price'].mean().reset_index()

    #####--------------- climate ---------------####
    th_temp = pd.read_csv("https://raw.githubusercontent.com/Plagrim-Apichaya/830_f23_midterm/main/TH_mean_temperature.csv")
    th_precip = pd.read_csv("https://raw.githubusercontent.com/Plagrim-Apichaya/830_f23_midterm/main/TH_precipitation.csv")

    th_temp_select = th_temp[(th_temp["year"] >= 2014) & (th_temp["year"] <= 2019)].reset_index()
    th_precip_select = th_precip[(th_precip["year"] >= 2014) & (th_precip["year"] <= 2019)].reset_index()

    corn_mean["Precipitation"] = th_precip_select["precipitation"]
    corn_mean["Mean Surface Temperature"] = th_temp_select["mean surface temperature"]

    rice_mean["Precipitation"] = th_precip_select["precipitation"]
    rice_mean["Mean Surface Temperature"] = th_temp_select["mean surface temperature"]

    cassava_mean["Precipitation"] = th_precip_select["precipitation"]
    cassava_mean["Mean Surface Temperature"] = th_temp_select["mean surface temperature"]

    # agri_type = ["Rice", "Corn", "Cassava"]
    def str_to_MainDF(agri_type):
        if agri_type == "Corn":
            agri_type_df = corn
            color = "orange"
        elif agri_type == "Rice":
            agri_type_df = rice
            color = "greenyellow"
        elif agri_type == "Cassava":
            agri_type_df = cassava
            color = "deepskyblue"
        return agri_type_df, color

    def detail_plot(agri_type, year = 2018):
        agri_type_df, color = str_to_MainDF(agri_type)
        select_year = agri_type_df[agri_type_df["year"] == year]
        chart_1 = alt.Chart(select_year).mark_line(color = color).encode(
            x = alt.X('date', title = 'Dates'),
            y = alt.Y(select_year.columns[-1], title = 'Price (Thai Baht)'),
            tooltip=['date', select_year.columns[-1]],
            strokeWidth = alt.value(4)
        ).properties(
            width = 600,
            height = 300,
        )

        chart_2 = alt.Chart(select_year).mark_point(color = "tomato", size = 150).encode(
            x = alt.X('date', title = 'Dates'),
            y = alt.Y(select_year.columns[-1], title = 'Price (Thai Baht)'),
            tooltip=['date', select_year.columns[-1]]
        )

        chart = chart_1 + chart_2
        return chart

    #option = ["Price", "Area", "Production"]
    def line_plot(option):
        if option == "Price":
            print("price")
            #------------------- a ----------------
            chart_a = alt.Chart(corn_mean).mark_line().encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('corn_price:Q', title = "Corn Price"),
                color = alt.value('orange'),
                tooltip = ['year', 'corn_price']
            ).properties(
                width = 150,
                height = 300,
                title = 'Corn'
            )
            point_a = alt.Chart(corn_mean).mark_point(color = 'tomato', size = 100).encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('corn_price:Q', title = "Corn Price")
            )
            a_plot = chart_a + point_a

            #------------------- b ----------------
            chart_b = alt.Chart(rice_mean).mark_line().encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('rice_price:Q', title = "Rice Price"),
                color = alt.value('greenyellow'),
                tooltip = ['year', 'rice_price']
            ).properties(
                width = 150,
                height = 300,
                title = 'Rice'
            )
            point_b = alt.Chart(rice_mean).mark_point(color = 'tomato', size = 100).encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('rice_price:Q', title = "Rice Price")
            )
            b_plot = chart_b + point_b

            #------------------- c ----------------
            chart_c = alt.Chart(cassava_mean).mark_line().encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('cassava_price:Q', title = "Cassava Price"),
                color = alt.value('deepskyblue'),
                tooltip = ['year', 'cassava_price']
            ).properties(
                width = 150,
                height = 300,
                title = 'Cassava'
            )
            point_c = alt.Chart(cassava_mean).mark_point(color = 'tomato', size = 100).encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('cassava_price:Q', title = "Cassava Price")
            )
            c_plot = chart_c + point_c

            combined_chart = alt.hconcat(a_plot, b_plot, c_plot).resolve_scale(y = 'shared')

        elif option == "Area":
            #------------------- a ----------------
            chart_a = alt.Chart(corn_mean).mark_line().encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Corn Area (1000 Ha):Q', title = "Corn Area (1000 Ha)"),
                color = alt.value('orange'),
                tooltip = ['year', 'Corn Area (1000 Ha)']
            ).properties(
                width = 150,
                height = 300,
                title = 'Corn'
            )
            point_a = alt.Chart(corn_mean).mark_point(color = 'tomato', size = 100).encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Corn Area (1000 Ha):Q', title = "Corn Area (1000 Ha)")
            )
            a_plot = chart_a + point_a

            #------------------- b ----------------
            chart_b = alt.Chart(rice_mean).mark_line().encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Rice Area (1000 Ha):Q', title = "Rice Area (1000 Ha)"),
                color = alt.value('greenyellow'),
                tooltip = ['year', 'Rice Area (1000 Ha)']
            ).properties(
                width = 150,
                height = 300,
                title = 'Rice'
            )
            point_b = alt.Chart(rice_mean).mark_point(color = 'tomato', size = 100).encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Rice Area (1000 Ha):Q', title = "Rice Area (1000 Ha)")
            )
            b_plot = chart_b + point_b

            combined_chart = alt.hconcat(a_plot, b_plot).resolve_scale(y = 'shared')

        elif option == "Production":
            #------------------- a ----------------
            chart_a = alt.Chart(corn_mean).mark_line().encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Corn Production (1000 Tons):Q', title = "Corn Production (1000 Tons)"),
                color = alt.value('orange'),
                tooltip = ['year', 'Corn Production (1000 Tons)']
            ).properties(
                width = 150,
                height = 300,
                title = 'Corn'
            )
            point_a = alt.Chart(corn_mean).mark_point(color = 'tomato', size = 100).encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Corn Production (1000 Tons):Q', title = "Corn Production (1000 Tons)")
            )
            a_plot = chart_a + point_a

            #------------------- b ----------------
            chart_b = alt.Chart(rice_mean).mark_line().encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Rice Production (1000 Tons):Q', title = "Rice Production (1000 Tons)"),
                color = alt.value('greenyellow'),
                tooltip = ['year', 'Rice Production (1000 Tons)']
            ).properties(
                width = 150,
                height = 300,
                title = 'Rice'
            )
            point_b = alt.Chart(rice_mean).mark_point(color = 'tomato', size = 100).encode(
                x = alt.X('year', title = "Year"),
                y = alt.Y('Rice Production (1000 Tons):Q', title = "Rice Production (1000 Tons)")
            )
            b_plot = chart_b + point_b

            combined_chart = alt.hconcat(a_plot, b_plot).resolve_scale(y = 'shared')
        return combined_chart

    def heatmap(option):
        cor_data = (option.corr().stack()
                    .reset_index()     # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
                    .rename(columns={0: 'correlation', 'level_0': 'variable1', 'level_1': 'variable2'}))
        cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal

        base = alt.Chart(cor_data).encode(
            x = 'variable2:O',
            y = 'variable1:O'
        )

        text = base.mark_text().encode(
            text = 'correlation_label',
            color = alt.condition(
                alt.datum.correlation > 0.5,
                alt.value('white'),
                alt.value('black')
            ), tooltip=['variable2', 'variable1', 'correlation']
        )

        # The correlation heatmap
        cor_plot = base.mark_rect().encode(
            alt.Color('correlation:Q', scale = alt.Scale(scheme = 'redblue'),
                    ),
            tooltip = ['variable2', 'variable1', 'correlation']
        )

        larger_figure = (cor_plot + text).properties(
            width = 600,
            height = 600
        )

        return larger_figure

    def precip_plot(agri_type):
        bin_width = 0.5
        chart_1 = alt.Chart(corn_mean).mark_bar(color = "lightskyblue").encode(
            x = alt.X('year:O', bin = alt.Bin(step = bin_width), title = 'Year'),
            y = 'Precipitation',
            tooltip = ['year', 'Precipitation']
        ).properties(
            width = 400,
            height = 400
        )

        chart_2 = alt.Chart(corn_mean).mark_line(color = "royalblue").encode(
            x = alt.X('year:O', bin = alt.Bin(step = bin_width), title = 'Year'),
            y = alt.Y('Mean Surface Temperature', scale = alt.Scale(domain = [25, 30])),
            tooltip = ['year', 'Mean Surface Temperature'],
            strokeWidth = alt.value(3)
        ).properties(
            width = 400,
            height = 400
        )

        chart_3 = alt.Chart(corn_mean).mark_point(filled = False, color = "tomato", size = 100).encode(
            x = alt.X('year:O', bin = alt.Bin(step = bin_width), title = 'Year'),
            y = alt.Y('Mean Surface Temperature', scale = alt.Scale(domain = [25, 30])),
            tooltip = ['year', 'Mean Surface Temperature']
        ).properties(
            width = 400,
            height = 400
        )

        dual_axis_chart = alt.layer(chart_1, chart_2, chart_3).resolve_scale(y = 'independent')

        return dual_axis_chart

    ########## -------------- Page arrangement -------------- ##########
    ########## ---------------------------------------------- ##########


    
    st.title('E-BOOK FARM')

    if st.session_state.validasi:    
        
        page = st.sidebar.radio("Menu",["Home","Rice","Corn","Cassava", "Climate", "Prediksi"])
        search_query = st.text_input('Masukkan kata kunci untuk mencari')

        # Daftar konten yang akan dicari (contoh daftar)
        content_list = [
        "Analisis harga pertanian Thailand dan faktor pendorong di balik dinamika harga.",
            "Pertanian terbaik di Thailand: Beras, Jagung, dan Singkong",
            "Project by: Sahid",
            """Web analisis data dengan data harga pertanian historis yang direkam setiap bulan dari Januari 2014 hingga Maret 2019\n
            Thailand adalah negara berkembang yang dinamis yang dikenal karena kontribusinya yang signifikan terhadap ekspor pertanian global. Negara ini merupakan pengekspor utama produk pertanian, dengan reputasi dalam memberikan budaya mereka bersama dengan produk tersebut seperti beras, buah-buahan, singkong, dan ikan. Ekspor pertanian ini tidak hanya memberikan dan melayani ekonomi negara tetapi juga berfungsi sebagai budaya dan tradisi Thailand. Selain itu, mereka memenuhi kebutuhan makanan penduduk Thailand. Namun, kenaikan harga-harga bahan pokok ini telah menimbulkan kekhawatiran dalam memahami dinamika rumit yang mengatur fluktuasinya.
            Aplikasi web ini akan membantu Anda menjelajahi dan menganalisis data harga pertanian historis yang tercatat dari Januari 2019 hingga Juni 2019. Hal ini juga untuk memahami dan meninjau tren dan pola dalam fluktuasi harga produk pertanian utama. Selain itu, tujuan kami adalah untuk menemukan faktor-faktor potensial yang memengaruhi dinamika harga pertanian utama di Thailand. Meskipun inflasi tidak diragukan lagi memainkan peran penting dalam mendorong perubahan harga, kami secara khusus tertarik untuk melihat dampak yang berbeda dari faktor-faktor lain yang berkontribusi.""",
            """Pemilihan Data\n
            Dataset inti untuk proyek ini akan berfokus pada tiga produk pertanian yang mendasar: singkong, beras, dan jagung. Catatan harga bulanan di Bangkok dari Januari 2014 hingga Juni 2019 akan dianalisis. Selain set data utama ini, kami akan menggabungkan tiga set data yang berbeda, yang masing-masing memiliki potensi untuk memengaruhi harga pertanian dan inflasi.""",
            """Faktor-faktor yang Mempengaruhi Dinamika Harga\n
            Untuk lebih jelasnya, Anda dapat memilih Menu bar untuk mengeksplorasi lebih lanjut tentang korelasi antara faktor variabel dan harga produk pertanian.
            1. Dataset Perubahan Penggunaan dan Tutupan Lahan: Memahami evolusi penggunaan dan tutupan lahan pertanian selama dua dekade terakhir sangatlah penting. Dataset ini akan memberikan wawasan tentang pergeseran area pertanian dari setiap produk dan memahami dampak dari kebijakan pertanian pemerintah di tahun-tahun yang berbeda.
            2. Statistik Produksi Pertanian: Statistik produksi tahunan/bulanan sangat penting dalam membentuk harga yang akan menilai bagaimana variasi dalam produksi pertanian berdampak pada dinamika harga.
            3. Catatan Curah Hujan Bulanan: Iklim Thailand ditandai dengan musim hujan dan musim kemarau, yang dapat sangat mempengaruhi produktivitas pertanian. Dengan menganalisis catatan curah hujan bulanan, kami bertujuan untuk memahami bagaimana variasi iklim berkorelasi dengan fluktuasi harga pangan.""",
            """Informasi dan analisis umum beras\n
            Beras adalah hasil panen utama bagi Thailand. Masyarakat Thailand mengonsumsi nasi hampir setiap hari.
            Thailand adalah produsen dan eksportir beras global yang terkemuka, dengan lahan pertanian yang luas mencapai 11 juta hektar dan berkontribusi lebih dari 30% volume perdagangan beras dunia pada tahun 2009. Pemerintah memperkenalkan skema penjaminan beras pada tahun 2011 untuk mendukung para petani dengan menawarkan harga yang lebih tinggi dari harga pasar untuk beras mereka.
            Meskipun panen beras berkurang di tahun 2014, penjualan yang berkelanjutan dari cadangan beras Pemerintah diharapkan dapat meningkatkan ekspor, dan berpotensi untuk mendapatkan kembali status eksportir terbesar di tahun 2015. Meskipun begitu, sektor beras menghadapi tantangan-tantangan keberlanjutan karena produktivitas yang rendah, kekurangan tenaga kerja, dan kelangkaan air.
            Padi di Thailand terutama ditanam selama musim hujan (75% tadah hujan, 25% irigasi) dan musim kemarau. Perubahan iklim, yang memengaruhi suhu dan curah hujan, menimbulkan risiko bagi sistem pertanian tadah hujan. Strategi adaptasi melibatkan perubahan praktik pertanian, peningkatan pengelolaan air, diversifikasi pertanian, investasi dalam teknologi, dan penerapan asuransi dan manajemen risiko.
            Kekurangan air, yang terkait dengan perubahan iklim, menjadi hambatan yang signifikan untuk meningkatkan produksi. Karena perubahan iklim berdampak pada hasil panen beras dan pertumbuhan populasi global mengancam ketahanan pangan, industri beras Thailand harus mengatasi tantangan produksi dan beradaptasi dengan realitas perubahan iklim."""
            """Rice Every Meal, Nasi Setiap Kali Makan\n
            Makanan yang paling banyak dikonsumsi dan merupakan bagian penting dari masakan Thailand. Satu hal yang pasti, Anda tidak akan menemukan penduduk lokal yang makan tanpa nasi! Makanan ini dianggap memiliki jiwa tersendiri yang menyoroti pentingnya dalam budaya negara ini.
            Dilambangkan dengan Ibu Padi, yang lahir dari padi, kemudian hamil dan melahirkan lebih banyak padi, menciptakan siklus kehidupannya sendiri. Keutamaan beras juga ditekankan oleh fakta bahwa nasi adalah makanan pokok. Digunakan sebagai makanan yang dapat disiram dengan berbagai kari dan saus, tetapi juga dapat digunakan untuk membuat aneka masakan lainya."""
            """Our Best Rice, Beras Terbaik Kami\n
            Beras melati adalah varietas beras berkualitas premium yang banyak dibudidayakan di Thailand. Namun, diyakini bahwa hanya daerah-daerah tertentu, termasuk Provinsi Surin, Buriram, dan Sisaket, yang dapat menghasilkan beras berkualitas tinggi. Meskipun hasil panennya lebih rendah dibandingkan dengan jenis beras lainnya, beras melati memiliki harga yang jauh lebih tinggi di pasar global, sering kali dijual dengan harga dua kali lipat lebih tinggi dari harga komoditas beras lainnya."""
            """Ada banyak makanan Thailand yang lezat dan makanan penutup Thailand yang terbuat dari jagung.\n
            Jagung merupakan sumber makanan yang penting secara global dan salah satu tanaman utama di Thailand, mencakup sekitar 33% dari lahan pertanian dataran tinggi di negara tersebut, dengan pertumbuhan yang signifikan terlihat di Thailand bagian utara. Namun, praktik pasca panen yang melibatkan pembakaran terbuka yang meluas untuk membuang tongkol dan sekam jagung untuk persiapan lahan, mengakibatkan berbagai masalah bagi masyarakat lokal dan penduduk perkotaan.
            Jagung adalah salah satu dari lima tanaman utama di Thailand, bersama dengan beras, singkong, tebu, dan karet, yang mencakup sebagian besar (sekitar 33%) lahan pertanian dataran tinggi di negara tersebut. Pada tahun 2017, produksi jagung Thailand mencapai 41 juta ton, menunjukkan peningkatan sebesar 1,26% dari tahun sebelumnya. Peningkatan ini juga tercermin dari hasil panen jagung yang naik menjadi 4.500 kg/ha, menandai peningkatan 5,73% dari 4.256 kg/ha, sebagian karena dukungan dari Promosi Produksi Jagung Musim Kering setelah Proyek Tanaman Padi Utama Tahun 2017. Selain itu, kondisi curah hujan yang baik selama musim hujan juga berkontribusi pada peningkatan hasil panen jagung."""
            """Singkong digunakan untuk membuat tepung dan tentu saja makanan penutup tradisional Thailand yang lezat.\n
            Singkong adalah sayuran akar yang ditanam oleh Plantations International di Thailand. Ini adalah bagian bawah tanah dari semak singkong, yang memiliki nama latin Manihot esculenta. Seperti kentang dan ubi, singkong merupakan tanaman umbi-umbian. Akar singkong memiliki bentuk yang mirip dengan ubi jalar.
            Manusia juga dapat memakan daun tanaman singkong. Manusia yang tinggal di sepanjang tepi Sungai Amazon di Amerika Selatan telah menanam dan mengonsumsi singkong ratusan tahun sebelum Christopher Columbus pertama kali melakukan pelayaran ke sana.
            Singkong merupakan makanan pokok yang penting bagi lebih dari 800 juta orang di seluruh dunia, yang berfungsi sebagai komponen makanan utama di banyak negara, terutama di Afrika Sub-Sahara, di mana singkong merupakan sumber karbohidrat utama di antara tanaman pokok. Tanaman ini juga merupakan tanaman energi yang penting untuk produksi bioetanol dan sangat cocok untuk daerah tropis dataran rendah yang panas dan tanah yang menipis. Thailand adalah produsen dan pengekspor produk singkong utama dunia, menduduki peringkat pertama dalam nilai ekspor singkong segar dan pati ubi kayu selama dekade terakhir, dengan angka tahun 2019 yang menyumbang 62,32% dan 72,31% dari nilai ekspor global. Dalam hal produksi singkong dan area panen, Thailand berada di peringkat kedua dan ketiga secara global, menghasilkan 32 juta ton dari 1,38 juta hektar pada tahun 2018. Di tingkat lokal, sekitar 0,46 juta rumah tangga petani membudidayakan singkong, dengan satu juta hektar area panen, menjadikannya tanaman yang paling banyak dibudidayakan keempat di negara ini dalam hal penggunaan lahan pertanian."""
            """Iklim adalah masalah lain yang perlu dipertimbangkan\n
            Grafik ini merupakan grafik batang interaktif yang mewakili curah hujan (termasuk curah hujan) dalam mm per tahun, dan plot garis mewakili suhu permukaan rata-rata tahunan.
            Curah hujan tahunan rata-rata adalah 1.200-4.500 mm, dengan total yang lebih rendah di sisi bawah angin dan total yang lebih tinggi di sisi angin. Suhu rata-rata 26,3°C di bagian utara dan 27,5°C di bagian selatan dan pesisir.
            Pada tahun 2017, curah hujan yang tercatat merupakan yang tertinggi dibandingkan dengan tahun-tahun sebelumnya."""
            """THAILAND\n
            Thailand merupakan salah satu negara di Asia Tenggara yang terletak di dekat garis khatulistiwa. Ini adalah tujuan wisata impian bagi banyak wisatawan karena pemandangannya yang indah yang berpadu dengan budaya."""
            # Tambahkan konten lain sesuai kebutuhan
        ]

        # Tampilkan hasil pencarian jika tombol pencarian ditekan
        if st.button('Cari'):
            search_results = search_content(search_query, content_list)
            if search_results:
                st.subheader('Hasil Pencarian:')
                for result in search_results:
                    st.write(result)
            else:
                st.info('Tidak ada hasil pencarian.')

        #### ---- HOME ---- ####
        if page == "Home":

            st.image("https://c.tadst.com/gfx/600x337/international-year-plant-health.jpg?1", width = 600)
            st.subheader("Web analisis data dengan data harga pertanian historis yang direkam setiap bulan dari Januari 2014 hingga Maret 2019")
            st.write("Thailand adalah negara berkembang yang dinamis yang dikenal karena kontribusinya yang signifikan terhadap ekspor pertanian global. Negara ini merupakan pengekspor utama produk pertanian, dengan reputasi dalam memberikan budaya mereka bersama dengan produk tersebut seperti beras, buah-buahan, singkong, dan ikan. Ekspor pertanian ini tidak hanya memberikan dan melayani ekonomi negara tetapi juga berfungsi sebagai budaya dan tradisi Thailand. Selain itu, mereka memenuhi kebutuhan makanan penduduk Thailand. Namun, kenaikan harga-harga bahan pokok ini telah menimbulkan kekhawatiran dalam memahami dinamika rumit yang mengatur fluktuasinya.")
            st.markdown("Aplikasi web ini akan membantu Anda menjelajahi dan menganalisis data harga pertanian historis yang tercatat dari Januari 2019 hingga Juni 2019. Hal ini juga untuk memahami dan meninjau tren dan pola dalam fluktuasi harga produk pertanian utama. Selain itu, tujuan kami adalah untuk menemukan faktor-faktor potensial yang memengaruhi dinamika harga pertanian utama di Thailand. Meskipun inflasi tidak diragukan lagi memainkan peran penting dalam mendorong perubahan harga, kami secara khusus tertarik untuk melihat dampak yang berbeda dari faktor-faktor lain yang berkontribusi.")
            st.markdown("#### Pemilihan Data")
            st.write("Dataset inti untuk proyek ini akan berfokus pada tiga produk pertanian yang mendasar: singkong, beras, dan jagung. Catatan harga bulanan di Bangkok dari Januari 2014 hingga Juni 2019 akan dianalisis. Selain set data utama ini, kami akan menggabungkan tiga set data yang berbeda, yang masing-masing memiliki potensi untuk memengaruhi harga pertanian dan inflasi.")

            st.write("### Jelajahi dataset")
            raw = st.checkbox("Kumpulan data mentah harga produk pertanian Thailand Bulanan (2014 - 2019)")
            if raw == True:
                st.dataframe(df)
            describe = st.checkbox("Analisis deskriptif")
            if describe == True:
                st.dataframe(descriptive)

            st.markdown("#### Faktor-faktor yang Mempengaruhi Dinamika Harga")
            st.write("Untuk lebih jelasnya, Anda dapat memilih Menu bar untuk mengeksplorasi lebih lanjut tentang korelasi antara faktor variabel dan harga produk pertanian.")
            st.markdown("1. Dataset Perubahan Penggunaan dan Tutupan Lahan: Memahami evolusi penggunaan dan tutupan lahan pertanian selama dua dekade terakhir sangatlah penting. Dataset ini akan memberikan wawasan tentang pergeseran area pertanian dari setiap produk dan memahami dampak dari kebijakan pertanian pemerintah di tahun-tahun yang berbeda.")
            st.markdown("2. Statistik Produksi Pertanian: Statistik produksi tahunan/bulanan sangat penting dalam membentuk harga yang akan menilai bagaimana variasi dalam produksi pertanian berdampak pada dinamika harga.")
            st.markdown("3. Catatan Curah Hujan Bulanan: Iklim Thailand ditandai dengan musim hujan dan musim kemarau, yang dapat sangat mempengaruhi produktivitas pertanian. Dengan menganalisis catatan curah hujan bulanan, kami bertujuan untuk memahami bagaimana variasi iklim berkorelasi dengan fluktuasi harga pangan.")

            st.write("### Memulai analisis data")
            st.write("#### Harga, Luas Panen, dan Jumlah Produksi Padi, Jagung, dan Ubi Kayu")
            option = st.selectbox("Silakan pilih opsi di bawah ini", ["Price", "Area", "Production"])
            option = str(option)
            fig = line_plot(option)
            st.altair_chart(fig)

            st.write("#### Pendalaman harga Beras, Jagung, dan Singkong tahunan. Anda dapat menyesuaikan tahun untuk memulai analisis")
            agri_type = st.selectbox("Pilihlah jenis produk pertanian dari daftar di bawah ini.", ["Rice", "Corn", "Cassava"])
            year = st.slider("Year", min_value = 2014, max_value = 2019, value = 2018, step = 1)
            fig2 = detail_plot(agri_type, year)
            st.altair_chart(fig2)

        #### ---- RICE ---- ####
        elif page == "Rice":
            st.write("### Informasi dan analisis umum beras")
            st.image("https://news.thaipbs.or.th/media/TSNBg3wSBdng7ijMho7k51Nzv9MyniZjx4TdAN0izb3.jpg")
            st.write("#### Beras adalah hasil panen utama bagi Thailand. Masyarakat Thailand mengonsumsi nasi hampir setiap hari.")

            col1, col2 = st.columns(2)
            with col1:
                st.image("https://ipad.fas.usda.gov/countrysummary/images/TH/cropprod/TH_Rice.png", width = 350)
            with col2:
                st.write("## ")
                st.write("Thailand adalah produsen dan eksportir beras global yang terkemuka, dengan lahan pertanian yang luas mencapai 11 juta hektar dan berkontribusi lebih dari 30% volume perdagangan beras dunia pada tahun 2009. Pemerintah memperkenalkan skema penjaminan beras pada tahun 2011 untuk mendukung para petani dengan menawarkan harga yang lebih tinggi dari harga pasar untuk beras mereka.")
                st.write("Meskipun panen beras berkurang di tahun 2014, penjualan yang berkelanjutan dari cadangan beras Pemerintah diharapkan dapat meningkatkan ekspor, dan berpotensi untuk mendapatkan kembali status eksportir terbesar di tahun 2015. Meskipun begitu, sektor beras menghadapi tantangan-tantangan keberlanjutan karena produktivitas yang rendah, kekurangan tenaga kerja, dan kelangkaan air.")
            st.write("## ")
            st.write("Padi di Thailand terutama ditanam selama musim hujan (75% tadah hujan, 25% irigasi) dan musim kemarau. Perubahan iklim, yang memengaruhi suhu dan curah hujan, menimbulkan risiko bagi sistem pertanian tadah hujan. Strategi adaptasi melibatkan perubahan praktik pertanian, peningkatan pengelolaan air, diversifikasi pertanian, investasi dalam teknologi, dan penerapan asuransi dan manajemen risiko.")
            st.write("Kekurangan air, yang terkait dengan perubahan iklim, menjadi hambatan yang signifikan untuk meningkatkan produksi. Karena perubahan iklim berdampak pada hasil panen beras dan pertumbuhan populasi global mengancam ketahanan pangan, industri beras Thailand harus mengatasi tantangan produksi dan beradaptasi dengan realitas perubahan iklim.")
            st.write("## ")

            st.write("### Peta panas korelasi beras pada tahun 2014 - 2019 dengan faktor pendorong yang mempengaruhi harga.")
            st.write("### ")
            fig = heatmap(rice_mean)
            st.altair_chart(fig)
            st.write("### ")
            st.write("")

            fact = st.selectbox("Fakta tentang Beras di Thailand", ["Select here", "Rice Every Meal", "Our Best Rice"])

            if fact == "Rice Every Meal":
                st.write("Makanan yang paling banyak dikonsumsi dan merupakan bagian penting dari masakan Thailand. Satu hal yang pasti, Anda tidak akan menemukan penduduk lokal yang makan tanpa nasi! Makanan ini dianggap memiliki jiwa tersendiri yang menyoroti pentingnya dalam budaya negara ini.")
                st.write("Dilambangkan dengan Ibu Padi, yang lahir dari padi, kemudian hamil dan melahirkan lebih banyak padi, menciptakan siklus kehidupannya sendiri. Keutamaan beras juga ditekankan oleh fakta bahwa nasi adalah makanan pokok. Digunakan sebagai makanan yang dapat disiram dengan berbagai kari dan saus, tetapi juga dapat digunakan untuk membuat aneka masakan lainya.")
            elif fact == "Our Best Rice":
                st.write("Jasmine rice, known as ข้าวหอมมะลิ (khao hom mali) in Thai, is a premium-quality rice variety extensively cultivated in Thailand. However, it is believed that only specific regions, including Surin, Buriram, and Sisaket Provinces, can produce high-quality hom mali rice. Despite its lower crop yield compared to other rice types, jasmine rice commands a significantly higher price in the global market, often selling for more than double the price of other rice cultivars.")
            elif fact == "Select here":
                st.write("  ")

        #### ---- CORN ---- ####
        elif page == "Corn":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("https://www.ตลาดเกษตรกรออนไลน์.com/uploads/products/images/img_6423d9b84d507.jpg", width = 225)
            with col2:
                st.image("https://i.pinimg.com/1200x/0b/5e/34/0b5e349d855baea9ae2c46c46ebc3b94.jpg", width = 230)
            with col3:
                st.image("https://faprathanfarm.co.th/tinymce/uploaded/Product/veggie/P44.jpg", width = 182)
            st.write("### Jagung adalah tanaman utama kedua yang kami tanam. Ada banyak makanan Thailand yang lezat dan makanan penutup Thailand yang terbuat dari jagung.")

            col1, col2 = st.columns(2)
            with col1:
                st.image("https://ipad.fas.usda.gov/countrysummary/images/TH/cropprod/TH_Corn.png")
            with col2:
                st.write("## ")
                st.write("Jagung merupakan sumber makanan yang penting secara global dan salah satu tanaman utama di Thailand, mencakup sekitar 33% dari lahan pertanian dataran tinggi di negara tersebut, dengan pertumbuhan yang signifikan terlihat di Thailand bagian utara. Namun, praktik pasca panen yang melibatkan pembakaran terbuka yang meluas untuk membuang tongkol dan sekam jagung untuk persiapan lahan, mengakibatkan berbagai masalah bagi masyarakat lokal dan penduduk perkotaan.")

            st.write("## ")
            st.write("Jagung adalah salah satu dari lima tanaman utama di Thailand, bersama dengan beras, singkong, tebu, dan karet, yang mencakup sebagian besar (sekitar 33%) lahan pertanian dataran tinggi di negara tersebut. Pada tahun 2017, produksi jagung Thailand mencapai 41 juta ton, menunjukkan peningkatan sebesar 1,26% dari tahun sebelumnya. Peningkatan ini juga tercermin dari hasil panen jagung yang naik menjadi 4.500 kg/ha, menandai peningkatan 5,73% dari 4.256 kg/ha, sebagian karena dukungan dari Promosi Produksi Jagung Musim Kering setelah Proyek Tanaman Padi Utama Tahun 2017. Selain itu, kondisi curah hujan yang baik selama musim hujan juga berkontribusi pada peningkatan hasil panen jagung.")
            st.write("## ")
            st.write("### Peta panas korelasi jagung pada tahun 2014 - 2019 dengan faktor pendorong yang mempengaruhi harga.")
            st.write("### ")
            fig = heatmap(corn_mean)
            st.altair_chart(fig)

        #### ---- CASSAVA ---- ####
        elif page == "Cassava":

            col1, col2 = st.columns(2)
            with col1:
                st.image("https://www.czapp.com/wp-content/uploads/2022/11/7c6a62ad-01a4-4b41-a6a0-712bd3e137fa.jpg", width = 350)
            with col2:
                st.image("https://www.opt-news.com/public/upload/news/newsa23aab22b4cd1cc9c9a8aa7194847764.jpg", width = 325)

            st.write("### Singkong digunakan untuk membuat tepung dan tentu saja makanan penutup tradisional Thailand yang lezat.")
            st.write("## ")
            st.write("Singkong adalah sayuran akar yang ditanam oleh Plantations International di Thailand. Ini adalah bagian bawah tanah dari semak singkong, yang memiliki nama latin Manihot esculenta. Seperti kentang dan ubi, singkong merupakan tanaman umbi-umbian. Akar singkong memiliki bentuk yang mirip dengan ubi jalar.")
            st.write("Manusia juga dapat memakan daun tanaman singkong. Manusia yang tinggal di sepanjang tepi Sungai Amazon di Amerika Selatan telah menanam dan mengonsumsi singkong ratusan tahun sebelum Christopher Columbus pertama kali melakukan pelayaran ke sana.")
            st.write("Singkong merupakan makanan pokok yang penting bagi lebih dari 800 juta orang di seluruh dunia, yang berfungsi sebagai komponen makanan utama di banyak negara, terutama di Afrika Sub-Sahara, di mana singkong merupakan sumber karbohidrat utama di antara tanaman pokok. Tanaman ini juga merupakan tanaman energi yang penting untuk produksi bioetanol dan sangat cocok untuk daerah tropis dataran rendah yang panas dan tanah yang menipis. Thailand adalah produsen dan pengekspor produk singkong utama dunia, menduduki peringkat pertama dalam nilai ekspor singkong segar dan pati ubi kayu selama dekade terakhir, dengan angka tahun 2019 yang menyumbang 62,32% dan 72,31% dari nilai ekspor global. Dalam hal produksi singkong dan area panen, Thailand berada di peringkat kedua dan ketiga secara global, menghasilkan 32 juta ton dari 1,38 juta hektar pada tahun 2018. Di tingkat lokal, sekitar 0,46 juta rumah tangga petani membudidayakan singkong, dengan satu juta hektar area panen, menjadikannya tanaman yang paling banyak dibudidayakan keempat di negara ini dalam hal penggunaan lahan pertanian.")
            st.write("## ")
            st.write("### Peta panas korelasi singkong pada tahun 2014 - 2019 dengan faktor pendorong yang mempengaruhi harga.")
            st.write("### ")
            fig = heatmap(cassava_mean)
            st.altair_chart(fig)

        #### ---- CLIMATE ---- ####
        elif page == "Climate":
            st.image("https://thepattayanews.com/wp-content/uploads/2023/05/5ff66a95ac7c84ed5b190efba0db9b1d-1.jpg?v=1684740443")
            st.write("### Iklim adalah masalah lain yang perlu dipertimbangkan")
            st.write("### ")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Grafik ini merupakan grafik batang interaktif yang mewakili curah hujan (termasuk curah hujan) dalam mm per tahun, dan plot garis mewakili suhu permukaan rata-rata tahunan.")
                st.write("Curah hujan tahunan rata-rata adalah 1.200-4.500 mm, dengan total yang lebih rendah di sisi bawah angin dan total yang lebih tinggi di sisi angin. Suhu rata-rata 26,3°C di bagian utara dan 27,5°C di bagian selatan dan pesisir.")
                st.write("Pada tahun 2017, curah hujan yang tercatat merupakan yang tertinggi dibandingkan dengan tahun-tahun sebelumnya.")
            with col2:
                fig = precip_plot(cassava_mean)
                st.altair_chart(fig)

        #### ---- PREDIKSI ---- ####
        elif page == "Prediksi":
            st.image("https://static.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/lombokpost/2022/10/pertanian-.jpg")
            st.write("Negara Thailand memiliki kontribusi yang besar untuk ekspor pertanian global. Meskipun adanya inflasi tidak diragukan lagi memainkan peran penting dalam mendorong perubahan harga. Disini kita menyediakan informasi yang terbaik tentang makanan pokok yaitu Jagung, Padi dan singkong, untuk membantu pertanian Indonesia agar dapat mengurangi gagal panen jumlah besar yang dapat mengalami kerugian dan pemberdayaan masyarakat mandiri menjadi fokus dalam mengembangan kualitas pertanian.")
            st.markdown("Pertanian memiliki peran penting dalam pembangunan Indonesia. Sebagai negara agraris, Indonesia memiliki potensi pertanian yang besar di berbagai wilayahnya. Namun konversi lahan pertanian menjadi wilayah pemukiman dapat berdampak negatif terhadap produksi pangan. Oleh karena itu, pembangunan pertanian berkelanjutan menjadi sangat penting untuk menjaga keseimbangan antara pengembangan wilayah dan produksi pangan. Teknologi inovatif juga diperlukan untuk meningkatkan efisiensi produksi, nilai tambah, dan daya saing hasil pertanian.")

            Data = {
                "Sumatera": {
                    "Kemarau": ["Dataran Rendah", "Dataran Tinggi"],
                    "Penghujan": ["Dataran Rendah", "Dataran Tinggi"],
                },

                "Jawa": {
                    "Kemarau": ["Dataran Rendah", "Dataran Tinggi"],
                    "Penghujan": ["Dataran Rendah", "Dataran Tinggi"],
                },

                "Kalimantan": {
                    "Kemarau": ["Dataran Rendah", "Dataran Tinggi"],
                    "Penghujan": ["Dataran Rendah", "Dataran Tinggi"],
                },

                "Sulawesi": {
                    "Kemarau": ["Dataran Rendah", "Dataran Tinggi"],
                    "Penghujan": ["Dataran Rendah", "Dataran Tinggi"],
                },

                "Papua": {
                    "Kemarau": ["Dataran Rendah", "Dataran Tinggi"],
                    "Penghujan": ["Dataran Rendah", "Dataran Tinggi"],
                }

            }


            st.title('Selamat Datang di Prediksi Pertanian Di Indonesia ')

            if 'isClicked' not in st.session_state:
                st.session_state.isClicked = False

            if 'data' not in st.session_state:
                st.session_state.data = []

            #st.write(st.session_state.data)

            st.session_state.q1 = st.multiselect("Pilih Pulau", list(Data.keys()))
            if len(st.session_state.data) == 0:
                st.session_state.data.extend(st.session_state.q1)

            if st.session_state.q1:
                st.session_state.q2 = st.multiselect(f"Musim {st.session_state.q1[0]}", list(Data[st.session_state.q1[0]].keys()))
                if len(st.session_state.data) == 1:
                    st.session_state.data.extend(st.session_state.q2)

                if st.session_state.q2:
                    st.session_state.q3 = st.multiselect(f"Daerah Pertanian {st.session_state.q2[0]}", Data[st.session_state.q1[0]][st.session_state.q2[0]])
                    if len(st.session_state.data) == 2:
                        st.session_state.data.extend(st.session_state.q3)


            col1, col2, col3 = st.columns(3)


            if st.button("Submit"):
                if st.session_state.data and 'Sumatera' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Kemarau:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        """)

                if st.session_state.data and 'Sumatera' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Kemarau:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        """)

                if st.session_state.data and 'Sumatera' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Penghujan:
        1.Pad: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2.Kelap: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3.Pisan: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4.Jeruk Lima: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5.Mangg: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        """)

                if st.session_state.data and 'Sumatera' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tingg di Musim Penghujan:
        1.Strawberr: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2.Kop: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3.Kentan: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4.Brokol: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5.Kaka: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        """)

                if st.session_state.data and 'Jawa' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Kemarau:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.

        """)

                if st.session_state.data and 'Jawa' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Kemarau:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.

        """)

                if st.session_state.data and 'Jawa' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Penghujan:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        """)

                if st.session_state.data and 'Jawa' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Penghujan:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        """)

                if st.session_state.data and 'Kalimantan' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Kemarau:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        """)

                if st.session_state.data and 'Kalimantan' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Kemarau:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        """)

                if st.session_state.data and 'Kalimantan' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Penghujan:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        6. Sawi Hijau: Sawi hijau dapat tumbuh dengan baik di daerah dataran rendah.
        7. Bayam: Bayam sangat mudah dibudidayakan pada dataran rendah.
        8. Kangkung: Kangkung dapat tumbuh dengan baik di daerah dataran rendah.
        """)

                if st.session_state.data and 'Kalimantan' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Penghujan:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        6. Selada: Selada termasuk sayuran yang dapat tumbuh subur di dataran tinggi dengan suhu yang dingin.
        """)

                if st.session_state.data and 'Sulawesi' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Kemarau:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        """)

                if st.session_state.data and 'Sulawesi' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Kemarau:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        """)

                if st.session_state.data and 'Sulawesi' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Penghujan:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        6. Sawi Hijau: Sawi hijau dapat tumbuh dengan baik di daerah dataran rendah.
        7. Bayam: Bayam sangat mudah dibudidayakan pada dataran rendah.
        8. Kangkung: Kangkung dapat tumbuh dengan baik di daerah dataran rendah.
        """)

                if st.session_state.data and 'Sulawesi' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Penghujan:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        6. Selada: Selada termasuk sayuran yang dapat tumbuh subur di dataran tinggi dengan suhu yang dingin.
        """)

                if st.session_state.data and 'Papua' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Kemarau:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        """)

                if st.session_state.data and 'Papua' in st.session_state.data and 'Kemarau' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Kemarau:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Kakao: Kakao adalah bahan dasar pembuatan coklat yang hanya bisa tumbuh subur di dataran tinggi.
        """)

                if st.session_state.data and 'Papua' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Rendah' in st.session_state.data:
                    st.error("""Dataran Rendah di Musim Penghujan:
        1. Padi: Padi adalah tanaman dataran rendah pertama yang sering dijumpai dan dibutuhkan.
        2. Kelapa: Pohon kelapa dapat tumbuh optimal di dataran rendah atau pada ketinggian 0-450 mdpl.
        3. Pisang: Pisang tidak membutuhkan perawatan khusus. Tanaman ini akan tumbuh dengan optimal di dataran rendah hingga ketinggian 1.300 mdpl.
        4. Jeruk Limau: Jeruk limau tumbuh subur di dataran rendah dengan cuaca hangat dan sinar matahari yang cukup.
        5. Mangga: Mangga adalah tanaman dataran rendah hingga menengah dengan ketinggian berkisar 0-500 mdpl.
        6. Sawi Hijau: Sawi hijau dapat tumbuh dengan baik di daerah dataran rendah.
        """)

                if st.session_state.data and 'Papua' in st.session_state.data and 'Penghujan' in st.session_state.data and 'Dataran Tinggi' in st.session_state.data:
                    st.error("""Dataran Tinggi di Musim Penghujan:
        1. Strawberry: Strawberry menjadi tanaman dataran tinggi yang identik dengan warna merah meronanya. Jika ingin menanam Strawberry, pastikan ketinggian tanah telah berada di atas 1.000 mdpl dengan curah hujan 600-800 mm per tahun.
        2. Kopi: Kopi menjadi tanaman dataran tinggi yang memiliki banyak manfaat. Selain dapat dinikmati rasa khasnya di tengah udara dingin, kopi juga dapat digunakan sebagai scrub atau masker untuk mempercantik kulit.
        3. Kentang: Kentang juga termasuk umbi-umbian yang dapat ditanam di dataran tinggi. Kentang menjadi salah satu makanan pokok di beberapa wilayah.
        4. Brokoli: Brokoli cocok ditanam di dataran tinggi dengan suhu yang dingin.
        5. Asparagus: Asparagus hanya bisa tumbuh dengan baik di dataran tinggi dengan ketinggian 800–2.000 m dpl dengan suhu 10–20°C[^10^].
        """)

    else :
        st.write("Anda Harus Login Terlebih Dahulu")
    # Buat area teks input untuk melakukan pencarian
    
if __name__ == "__main__":
    main()
