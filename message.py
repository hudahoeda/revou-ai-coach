import streamlit as st

st.success("Pahami untuk menentukan asisten yang sesuai dengan kebutuhanmu!")

st.markdown(
    """
    ## Selamat datang di RevoU AI Coach! 👋

    Perkenalkan aku Revo, AI Coach eksklusif yang udah dirancang khusus dengan mengikuti best practices RevoU. AI Coach terbagi menjadi beberapa asisten yang terbagi dalam 3 kategori utama dan bisa kamu pilih untuk memenuhi kebutuhan kamu, jadi persiapan menuju pekerjaan impian bakal lebih gampang dan terarah!
    
    ## Asisten Sesuai Kebutuhanmu

    ## A. Personal Branding Discovery

    Cocok buat kamu yang butuh memahami dan menonjolkan pengalaman relevan untuk membangun personal branding yang kuat.

    ### 1. 💼 Relevant Experiences Discovery
    * 🧐 **Apa ini?**: Asisten ini bakal bantu kamu mengidentifikasi dan mencatat semua pengalaman relevan yang kamu punya. Ini bakal ngebantu kamu paham skill apa yang bisa kamu angkat lebih tinggi.
    * 💡 **Cara Pakainya**: Cukup jawab beberapa pertanyaan tentang pengalaman kamu, dan asisten ini bakal kasih insight tentang skill yang bisa kamu tonjolkan.

    ### 2. 📱 Experience Detail Discovery
    * 🧐 **Apa ini?**: Asisten ini bakal bantu kamu mendalami detail dari pengalaman yang kamu punya, biar bisa kamu pakai sebagai aset personal branding dan info penting buat interview.
    * 💡 **Cara Pakainya**: Ceritakan pengalamanmu, dan asisten ini bakal bantu kamu menggali detail penting yang bisa jadi nilai tambah.

    ## B. Assets Content Crafting

    Ideal buat kamu yang butuh panduan menyusun dan memperbaiki konten aplikasi kerja agar sesuai standar RevoU.

    ### 1. 📋 About Me Preparation
    * 🧐 **Apa ini?**: Asisten ini siap bantu kamu menyusun dan memperbaiki bagian "About Me" biar sesuai standar RevoU dan menarik perhatian.
    * 💡 **Cara Pakainya**: Jawab beberapa pertanyaan, dan asisten ini bakal bantu kamu bikin "About Me" yang kuat dan sesuai standar.

    ### 2. 📋 Professional and Organizational Experience Crafting
    * 🧐 **Apa ini?**: Asisten ini bantu kamu menyusun dan memperbaiki pengalaman profesional dan organisasi kamu, supaya sesuai dengan standar RevoU.
    * 💡 **Cara Pakainya**: Berikan detail pengalaman kerja dan organisasi kamu, dan asisten ini bakal bantu kamu menulisnya dengan baik.

    ### 3. 🔧 Project Crafting
    * 🧐 **Apa ini?**: Asisten ini bantu kamu menyusun dan memperbaiki pengalaman proyek kamu, supaya terlihat profesional dan sesuai standar RevoU.
    * 💡 **Cara Pakainya**: Ceritakan proyek yang pernah kamu kerjakan, dan asisten ini akan bantu kamu merangkumnya dengan baik.

    ## C. Quality Application Support

    Tepat buat kamu yang butuh memastikan aplikasi dan komunikasimu terlihat profesional dan terpersonalisasi.

    ### 1. 📋 Assets Personalization
    * 🧐 **Apa ini?**: Asisten ini bantu kamu mempersonalisasi dokumen aplikasi (seperti CV ATS) sesuai dengan lowongan pekerjaan tertentu, biar aplikasi kamu lebih stand out.
    * 💡 **Cara Pakainya**: Upload CV ATS kamu, dan asisten ini bakal kasih saran personalisasi untuk tiap posisi yang kamu incar.

    ### 2. ✉️ Professional Communication
    * 🧐 **Apa ini?**: Asisten ini bantu kamu menyusun cover letter dan pesan lainnya dengan nada profesional, supaya komunikasi kamu terlihat berkualitas tinggi.
    * 💡 **Cara Pakainya**: Tulis pesan atau cover letter yang ingin kamu kirim, dan asisten ini bakal bantu kamu menyusunnya dengan nada profesional yang tepat.

    ## Cara Pakai Platform ini

    1. Login pakai Username dan Password yang diberikan RevoU.
    2. Pilih Asisten yang paling pas buat kebutuhan kamu.
    3. Ikuti Panduannya. Setiap langkah udah didesain biar kamu bisa selesaiin dengan cepat dan tepat.
    4. Tinjau Hasilnya dan sesuaikan kalau masih kurang puas.
    5. Simpan dan Gunakan hasil akhirnya buat aplikasi kerja nyata kamu.

    ## Ketentuan Umum
    
    * **Keamanan & Akurasi:**

    Untuk jaga-jaga, tautan eksternal bakal dibatasi. Tapi tenang aja, kamu tetap bisa unggah file sendiri sampai 200MB per file dalam format TXT atau PDF lewat tombol di sidebar kiri.
    """)

st.image("assets/tutor_1.png")
    
st.markdown(""" * **Simpan Obrolanmu:**""")           
st.markdown("""* Simpan Obrolanmu: Saat kamu berpindah tab asisten, obrolan kamu akan terpisah. Jika **Logout** diklik, maka seluruh obrolanmu akan otomatis ditutup. Jadi, jika butuh jangan lupa simpan percakapanmu dengan cara:""")
st.markdown("""            
1. **Salin & Tempel** obrolan ke catatan digital pribadimu.
2. **Unduh obrolan** dalam format **PDF** → Klik ⋮ di kanan atas > **“Print”** > **“Save as PDF”**
    - Hanya berlaku untuk 1 obrolan asisten
3. **Rekam layar** saat obrolan berlangsung dalam **WebM** format → Klik ⋮ di kanan atas > **“Record a screencast”**
    - Berlaku untuk beberapa obrolan asisten sekaligus
    - Untuk menghentikan rekaman, klik titik tiga > **“Stop Recording”** lalu klik **“Save video to disk”** untuk menyimpan rekaman layar.
""")

col1, col2 = st.columns(2)

with col1:
    st.image("assets/tutor_2.png", caption="Cara save chat sebagai PDF", width=200,)

with col2:
    st.image("assets/tutor_3.png",caption="Cara screenrecord chat", width=200)
    
st.markdown(
    """
    * **Pengawasan:**

    Aktivitas dan interaksi kamu bakal dipantau oleh RevoU. Kami berhak menghentikan aktivitas yang terindikasi penipuan, termasuk menjalankan beberapa sesi bersamaan.)""")
    
st.markdown("""
            Dengan Revo, nyiapin diri buat nyari kerja jadi kebantu banget! Yuk, mulai sekarang dan wujudkan karir impian kamu bareng kita! 🎯
    """)