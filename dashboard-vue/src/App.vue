<script setup>
import { computed, onMounted, ref } from 'vue'
import StatTile from './components/StatTile.vue'

const API_URL = 'http://127.0.0.1:8000/bahan'
const bahan = ref([])
const keadaan = ref('loading')
const queryPencarian = ref('')
const arahUrutan = ref('az')
const tampilkanForm = ref(false)
const namaBaru = ref('')
const kategoriBaru = ref('')
const stokBaru = ref('')
const satuanBaru = ref('')
const idSedangDiedit = ref(null)
const stokEdit = ref('')
const pesanAksi = ref('')
const jenisPesan = ref('sukses')

const bahanTersaring = computed(() => {
  const kataKunci = queryPencarian.value.toLowerCase().trim()
  if (!kataKunci) return bahan.value
  return bahan.value.filter(
    (item) =>
      item.nama_bahan.toLowerCase().includes(kataKunci) ||
      item.kategori.toLowerCase().includes(kataKunci),
  )
})

const bahanTerurut = computed(() =>
  [...bahanTersaring.value].sort((a, b) => {
    const hasil = a.nama_bahan.localeCompare(b.nama_bahan, 'id')
    return arahUrutan.value === 'az' ? hasil : -hasil
  }),
)

const totalBahan = computed(() => bahan.value.length)
const stokMenipisHabis = computed(() => bahan.value.filter((item) => item.stok <= 3).length)
const jumlahKategori = computed(() => new Set(bahan.value.map((item) => item.kategori)).size)
const totalStok = computed(() => bahan.value.reduce((total, item) => total + item.stok, 0))

const stokPerKategori = computed(() => {
  const totalKategori = bahan.value.reduce((hasil, item) => {
    hasil[item.kategori] = (hasil[item.kategori] || 0) + item.stok
    return hasil
  }, {})
  const terbesar = Math.max(0, ...Object.values(totalKategori))
  return Object.entries(totalKategori).map(([kategori, stok]) => ({
    kategori,
    stok,
    persentase: terbesar === 0 ? 0 : (stok / terbesar) * 100,
  }))
})

function tampilkanPesan(teks, jenis = 'sukses') {
  pesanAksi.value = teks
  jenisPesan.value = jenis
}

function validasiStok(nilai) {
  return Number.isInteger(nilai) && nilai >= 0
}

async function muatBahan() {
  keadaan.value = 'loading'
  pesanAksi.value = ''
  try {
    const response = await fetch(API_URL)
    if (!response.ok) throw new Error(`Status HTTP: ${response.status}`)
    bahan.value = await response.json()
    keadaan.value = 'success'
  } catch (error) {
    console.error('Gagal memuat bahan:', error)
    keadaan.value = 'error'
  }
}

async function tambahBahan() {
  if (
    !namaBaru.value.trim() ||
    !kategoriBaru.value.trim() ||
    !satuanBaru.value.trim() ||
    !validasiStok(stokBaru.value)
  ) {
    tampilkanPesan('Lengkapi data. Stok harus berupa bilangan bulat 0 atau lebih.', 'error')
    return
  }
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nama_bahan: namaBaru.value.trim(),
        kategori: kategoriBaru.value.trim(),
        stok: stokBaru.value,
        satuan: satuanBaru.value.trim(),
      }),
    })
    if (!response.ok) throw new Error(`Status HTTP: ${response.status}`)
    namaBaru.value = ''
    kategoriBaru.value = ''
    stokBaru.value = ''
    satuanBaru.value = ''
    tampilkanForm.value = false
    await muatBahan()
    tampilkanPesan('Bahan baku berhasil ditambahkan.')
  } catch (error) {
    console.error('Gagal menambah bahan:', error)
    tampilkanPesan('Gagal menambah bahan. Periksa backend dan data form.', 'error')
  }
}

function mulaiEdit(item) {
  idSedangDiedit.value = item.id
  stokEdit.value = item.stok
  pesanAksi.value = ''
}

function batalEdit() {
  idSedangDiedit.value = null
  stokEdit.value = ''
}

async function simpanStok(id) {
  if (!validasiStok(stokEdit.value)) {
    tampilkanPesan('Stok harus berupa bilangan bulat 0 atau lebih.', 'error')
    return
  }
  try {
    const response = await fetch(`${API_URL}/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ stok: stokEdit.value }),
    })
    if (!response.ok) throw new Error(`Status HTTP: ${response.status}`)
    batalEdit()
    await muatBahan()
    tampilkanPesan('Stok bahan berhasil diperbarui.')
  } catch (error) {
    console.error('Gagal memperbarui stok:', error)
    tampilkanPesan('Gagal memperbarui stok. Coba lagi.', 'error')
  }
}

async function hapusBahan(item) {
  if (!window.confirm(`Hapus ${item.nama_bahan}?`)) return
  try {
    const response = await fetch(`${API_URL}/${item.id}`, { method: 'DELETE' })
    if (!response.ok) throw new Error(`Status HTTP: ${response.status}`)
    await muatBahan()
    tampilkanPesan(`${item.nama_bahan} berhasil dihapus.`)
  } catch (error) {
    console.error('Gagal menghapus bahan:', error)
    tampilkanPesan('Gagal menghapus bahan. Coba lagi.', 'error')
  }
}

function statusStok(stok) {
  if (stok === 0) return 'Stok Habis'
  if (stok <= 3) return 'Menipis'
  return 'Aman'
}

function kelasStatus(stok) {
  if (stok === 0) return 'status-habis'
  if (stok <= 3) return 'status-menipis'
  return 'status-aman'
}

onMounted(muatBahan)
</script>

<template>
  <header class="app-header">
    <div class="header-content">
      <h1>Dashboard Restoran</h1>
      <p>Data Bahan Baku Dapur</p>
    </div>
  </header>
  <main class="app-main">
    <section class="stat-grid" aria-label="Ringkasan bahan baku">
      <StatTile judul="Total Bahan Baku" :nilai="totalBahan" catatan="Jenis bahan terdaftar" />
      <StatTile judul="Stok Menipis + Habis" :nilai="stokMenipisHabis" catatan="Stok 0 sampai 3" />
      <StatTile judul="Jumlah Kategori" :nilai="jumlahKategori" catatan="Kategori unik" />
      <StatTile judul="Total Satuan Stok" :nilai="totalStok" catatan="Jumlah angka lintas satuan" />
    </section>

    <section class="panel" aria-labelledby="daftar-bahan">
      <div class="toolbar">
        <label class="search-field"
          ><span class="sr-only">Cari bahan atau kategori</span
          ><input v-model="queryPencarian" type="search" placeholder="Cari bahan atau kategori..."
        /></label>
        <div class="sort-actions" aria-label="Urutkan nama bahan">
          <button :class="{ active: arahUrutan === 'az' }" type="button" @click="arahUrutan = 'az'">
            A-Z</button
          ><button
            :class="{ active: arahUrutan === 'za' }"
            type="button"
            @click="arahUrutan = 'za'"
          >
            Z-A
          </button>
        </div>
        <button class="button primary" type="button" @click="tampilkanForm = !tampilkanForm">
          {{ tampilkanForm ? 'Tutup Form' : 'Tambah Bahan' }}
        </button>
        <button class="button secondary" type="button" @click="muatBahan">Muat Ulang</button>
      </div>

      <form v-if="tampilkanForm" class="add-form" @submit.prevent="tambahBahan">
        <label>Nama bahan<input v-model="namaBaru" type="text" required /></label
        ><label>Kategori<input v-model="kategoriBaru" type="text" required /></label
        ><label
          >Stok<input v-model.number="stokBaru" type="number" min="0" step="1" required /></label
        ><label
          >Satuan<input v-model="satuanBaru" type="text" placeholder="Contoh: kg" required /></label
        ><button class="button primary" type="submit">Simpan Bahan</button>
      </form>
      <p v-if="pesanAksi" class="action-message" :class="`message-${jenisPesan}`" role="status">
        {{ pesanAksi }}
      </p>
      <h2 id="daftar-bahan">Daftar Bahan Baku</h2>
      <p v-if="keadaan === 'loading'" class="state-message">Memuat data bahan baku...</p>
      <p v-else-if="keadaan === 'error'" class="state-message state-error">
        Gagal memuat data. Pastikan backend berjalan.
      </p>
      <p v-else-if="bahan.length === 0" class="state-message">Belum ada bahan baku.</p>
      <p v-else-if="bahanTerurut.length === 0" class="state-message">Bahan tidak ditemukan.</p>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nama Bahan</th>
              <th>Kategori</th>
              <th>Stok</th>
              <th>Satuan</th>
              <th>Status</th>
              <th>Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in bahanTerurut" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.nama_bahan }}</td>
              <td>{{ item.kategori }}</td>
              <td>
                <div v-if="idSedangDiedit === item.id" class="edit-stock">
                  <input
                    v-model.number="stokEdit"
                    type="number"
                    min="0"
                    step="1"
                    aria-label="Stok baru"
                  /><button class="link-button save" type="button" @click="simpanStok(item.id)">
                    Simpan</button
                  ><button class="link-button" type="button" @click="batalEdit">Batal</button>
                </div>
                <span v-else>{{ item.stok }}</span>
              </td>
              <td>{{ item.satuan }}</td>
              <td>
                <span class="stock-status" :class="kelasStatus(item.stok)">{{
                  statusStok(item.stok)
                }}</span>
              </td>
              <td>
                <div class="row-actions">
                  <button class="link-button" type="button" @click="mulaiEdit(item)">
                    Edit Stok</button
                  ><button class="link-button delete" type="button" @click="hapusBahan(item)">
                    Hapus
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="panel category-panel" aria-labelledby="ringkasan-kategori">
      <div>
        <h2 id="ringkasan-kategori">Ringkasan Stok per Kategori</h2>
        <p class="section-note">
          Angka adalah penjumlahan stok lintas satuan sebagai indikator latihan.
        </p>
      </div>
      <p v-if="keadaan === 'success' && stokPerKategori.length === 0" class="state-message">
        Belum ada data kategori.
      </p>
      <div v-else class="bar-list">
        <div v-for="item in stokPerKategori" :key="item.kategori" class="bar-item">
          <div class="bar-label">
            <span>{{ item.kategori }}</span
            ><strong>{{ item.stok }}</strong>
          </div>
          <div class="bar-track">
            <div class="bar-value" :style="{ width: item.persentase + '%' }"></div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
