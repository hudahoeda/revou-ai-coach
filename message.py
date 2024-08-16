import streamlit as st

st.success("Select Coach to chat with")

st.markdown(
    """
    ## Selamat Datang di RevoU AI Coach! 👋

    Perkenalkan aku Revo, AI Coach eksklusif yang udah dirancang khusus dengan mengikuti best practices RevoU. AI Coach terbagi menjadi beberapa asisten yang bisa kamu pilih untuk memenuhi kebutuhan kamu, jadi persiapan menuju pekerjaan impian bakal lebih gampang dan terarah!
    
    ## Asisten Sesuai Kebutuhanmu
    
    1. **📝 About Me Preparation:** 
        - **🧐 Apa ini?:** Asisten ini bakal bantu kamu buat kenal nilai, kekuatan utama, sampai tujuan karir biar bikin bagian “About Me” atau Ringkasan yang efektif dan menarik untuk CV kamu.
        - **💡 Cara Pakainya:** Cukup jawab beberapa pertanyaan simpel dari kita, dan asisten ini bakal ngerangkum jawaban kamu jadi profil yang menonjol.
    
    2. **💼 Experience Crafting:** 
        - **🧐 Apa ini?:** Bingung gimana ceritain pengalaman kerja kamu? Asisten ini siap bantu kamu susun pengalaman kerja yang jelas dan pas banget buat posisi yang kamu incar.
        - **💡 Cara Pakainya:** Kasih tau info tentang pekerjaan sebelumnya, dan asisten ini bakal bantu kamu susun pengalaman kerja yang menarik dan relevan.
    
    3. **🔧 Project Experience Crafting:**  
        - **🧐 Apa ini?:** Pernah ikut proyek keren? Asisten ini bakal bantu kamu nulis pengalaman proyek itu biar kelihatan lebih profesional dan nyambung dengan kerjaan yang kamu mau.
        - **💡 Cara Pakainya:** Ceritain aja proyek yang pernah kamu kerjain, dan kita bantu kamu tulis dengan cara yang tepat.
    
    4. **📋 Quality Application Kit:**
        - **🧐 Apa ini?:** Pastikan semua dokumen aplikasi kamu udah top! Asisten ini bakal bantu cek dan perbaiki kesalahan di CV, surat lamaran, sampai portofolio kamu.
        - **💡 Cara Pakainya:** Upload dokumen kamu, dan asisten ini bakal kasih saran perbaikan atau langsung bantu benerin otomatis.
    
    5. **📄 Resume Reviewer:** 
        - **🧐 Apa ini?:** Dapetin feedback buat CV atau resume kamu dari asisten ini, biar kamu yakin resume kamu udah siap tempur.
        - **💡 Cara Pakainya:** Kirim CT ATS kamu, dan asisten ini bakal kasih review mendalam plus saran biar lebih bagus.
    
    ## Cara Pakai Platform ini
    
    1. Login pakai Username dan Password yang diberikan RevoU
    2. Pilih Asisten yang paling pas buat kebutuhan kamu.
    3. Ikuti Panduannya. Setiap langkah udah didesain biar kamu bisa selesaiin dengan cepat dan tepat.
    4. Tinjau Hasilnya dan sesuaikan kalau masih kurang puas.
    5. Simpan dan Gunakan hasil akhirnya buat aplikasi kerja nyata kamu.
    
    ## Ketentuan Umum
    
    * **Keamanan & Akurasi:** Untuk jaga-jaga, tautan eksternal bakal dibatasi. Tapi tenang aja, kamu tetap bisa unggah file sendiri sampai 200MB per file dalam format TXT atau PDF lewat tombol di sidebar kiri.
    """)

st.image("assets/tutor_1.png")
    
st.markdown(""" * **Simpan Obrolanmu:** Saat kamu pindah-pindah tab asisten, obrolan kamu otomatis bakal ditutup. Jadi, jangan lupa simpan percakapanmu dengan cara: """)

col1, col2 = st.columns(2)

with col1:
    st.image("assets/tutor_2.png")

with col2:
    st.markdown("""            
        1. Salin & Tempel obrolan ke catatan pribadimu.
        2. Unduh obrolan dalam format PDF. → Print
        3. Rekam layar saat obrolan berlangsung. → Record a screencast""")
    
st.markdown(
    """
    **Pengawasan:** 
    
    Aktivitas dan interaksi kamu bakal dipantau oleh RevoU. Kami berhak menghentikan aktivitas yang terindikasi penipuan, termasuk menjalankan beberapa sesi bersamaan.
    
    Dengan Revo, nyiapin diri buat nyari kerja jadi kebantu banget! Yuk, mulai sekarang dan wujudkan karir impian kamu bareng kita! 🎯

    """)