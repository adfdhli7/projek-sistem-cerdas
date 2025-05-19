import streamlit as st
from collections import defaultdict, Counter

# ==================== DATA LATIH ====================
data_latih = [
        # MAKANAN TIDAK PEDAS
     ['murah', 'tidak pedas', 'gurih', 'biasa', 'Indomie Goreng'],
      ['menengah', 'tidak pedas', 'gurih', 'populer', 'Indomie Rendang'],
       ['murah', 'tidak pedas', 'berkuah', 'biasa', 'Mie Sedap Soto'],
        ['murah', 'tidak pedas', 'kering', 'biasa', 'Tahu Telur'],
         ['menengah', 'tidak pedas', 'crispy', 'biasa', 'Ayam crispy'],
          ['murah', 'tidak pedas', 'berkuah', 'biasa', 'Mie Sedap Ayam Bawang'],
           ['murah', 'tidak pedas', 'kering', 'biasa', 'Nasi Goreng'],
            ['murah', 'tidak pedas', 'berkuah', 'populer', 'Mie Ayam'],
             ['menengah', 'tidak pedas', 'berkuah', 'biasa', 'Mie Ayam Jumbo'],
              ['mahal', 'tidak pedas', 'berkuah', 'biasa', 'Mie Ayam Jumbo + katsu'],
               ['murah', 'tidak pedas', 'gurih', 'populer', 'Mie yamin'],
                ['mahal', 'tidak pedas', 'gurih', 'populer', 'Mie yamin Jumbo + katsu'],
    # MAKANAN SEDANG
     ['murah', 'sedang', 'kering', 'biasa', 'Tahu Telur'],
      ['murah', 'sedang', 'kering', 'biasa', 'Nasi Goreng'],
       ['murah', 'sedang', 'berkuah', 'populer', 'Mie Ayam'],
        ['menengah', 'sedang', 'berkuah', 'biasa', 'Mie Ayam Jumbo'],
         ['mahal', 'sedang', 'berkuah', 'biasa', 'Mie Ayam Jumbo + katsu'],
          ['murah', 'sedang', 'gurih', 'populer', 'Mie yamin'],
           ['mahal','sedang', 'gurih', 'populer', 'Mie yamin Jumbo + katsu'],
            ['murah', 'sedang', 'gurih', 'populer', 'Mie yamin'],
             ['mahal', 'sedang', 'gurih', 'populer', 'Mie yamin Jumbo + katsu'],
    # MAKANAN PEDAS
     ['murah', 'pedas', 'gurih', 'populer', 'Indomie Ayam Geprek'],
      ['menengah', 'tidak pedas', 'crispy', 'biasa', 'Katsu Ayam'],
       ['menengah', 'pedas', 'kering', 'biasa', 'Nasi Gila'],
        ['mahal', 'pedas', 'kering', 'populer', 'Nasi Gila + katsu'],
         ['murah', 'pedas', 'kering', 'biasa', 'Tahu Telur'],
          ['murah', 'pedas', 'kering', 'biasa', 'Nasi Goreng'],
           ['murah', 'pedas', 'berkuah', 'populer', 'Mie Ayam'],
            ['menengah', 'pedas', 'berkuah', 'biasa', 'Mie Ayam Jumbo'],
             ['mahal', 'pedas', 'berkuah', 'biasa', 'Mie Ayam Jumbo + katsu'],
              ['murah', 'pedas', 'gurih', 'populer', 'Mie yamin'],
               ['mahal', 'pedas', 'gurih', 'populer', 'Mie yamin Jumbo + katsu'],
]

# ==================== NAIVE BAYES ====================
def train_naive_bayes(data_latih):
    total_data = len(data_latih)
    kelas_counter = Counter([d[4] for d in data_latih])
    fitur_counter = defaultdict(lambda: defaultdict(lambda: Counter()))

    for budget, selera, karakteristik, populer, makanan in data_latih:
        fitur_counter['budget'][budget][makanan] += 1
        fitur_counter['selera'][selera][makanan] += 1
        fitur_counter['karakteristik'][karakteristik][makanan] += 1
        fitur_counter['popularitas'][populer][makanan] += 1

    return fitur_counter, kelas_counter, total_data

def prediksi_naive_bayes(fitur_counter, kelas_counter, total_data, budget_input, selera_input, karakteristik_input, popularitas_input):
    hasil_prob = {}

    for makanan in kelas_counter:
        prob_makanan = kelas_counter[makanan] / total_data
        prob_budget = (fitur_counter['budget'][budget_input][makanan] + 1) / (kelas_counter[makanan] + 4)
        prob_selera = (fitur_counter['selera'][selera_input][makanan] + 1) / (kelas_counter[makanan] + 4)
        prob_karakteristik = (fitur_counter['karakteristik'][karakteristik_input][makanan] + 1) / (kelas_counter[makanan] + 4)
        prob_popularitas = (fitur_counter['popularitas'][popularitas_input][makanan] + 1) / (kelas_counter[makanan] + 4)

        total_prob = prob_makanan * prob_budget * prob_selera * prob_karakteristik * prob_popularitas
        hasil_prob[makanan] = total_prob

    rekomendasi_teratas = sorted(
        hasil_prob.items(),
        key=lambda x: (x[1], kelas_counter[x[0]]),
        reverse=True
    )[:3]

    return rekomendasi_teratas

# ==================== STREAMLIT UI ====================
st.title("Rekomendasi Makanan Kantin Filkom UB🍴")

nama = st.text_input("Masukkan namamu:")

budget_input = st.selectbox("Berapa budget kamu?", ['murah', 'menengah', 'mahal'])
selera_input = st.selectbox("Kamu suka makanan?", ['tidak pedas', 'sedang', 'pedas'])
karakteristik_input = st.selectbox("Karakteristik makanan yang kamu suka:", ['crispy', 'gurih', 'berkuah', 'kering'])
populer_bool = st.radio("Mau makanan yang populer?", ['Ya', 'Tidak'])
popularitas_input = 'populer' if populer_bool == 'Ya' else 'biasa'

if st.button("🔍 Cari Rekomendasi"):
    fitur_counter, kelas_counter, total_data = train_naive_bayes(data_latih)
    hasil = prediksi_naive_bayes(fitur_counter, kelas_counter, total_data,
                                 budget_input, selera_input, karakteristik_input, popularitas_input)

    st.subheader(f"Halo {nama} 👋, ini rekomendasi buat kamu:")
    for nama_makanan, skor in hasil:
        st.markdown(f"- **{nama_makanan}** (Skor: `{skor:.6f}`)")

    if hasil:
        st.success(f"👉 Rekomendasi utama: **{hasil[0][0]}** 🍽️")
