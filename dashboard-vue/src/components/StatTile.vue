<script setup>
defineProps({
  judul: { type: String, required: true },
  nilai: { type: [String, Number], required: true },
  catatan: { type: String, required: true },
})
</script>

<template>
  <article class="stat-tile">
    <p class="stat-title">{{ judul }}</p>
    <p class="stat-value">{{ nilai }}</p>
    <p class="stat-note">{{ catatan }}</p>
  </article>
</template>

<style scoped>
.stat-tile {
  min-width: 0;
  padding: 1.1rem;
  background: #fff;
  border: 1px solid #dce6e9;
  border-radius: 8px;
}
.stat-title,
.stat-note {
  margin: 0;
}
.stat-title {
  color: #46606b;
  font-size: 0.88rem;
}
.stat-value {
  margin: 0.35rem 0;
  color: #0b4f6c;
  font-size: 1.75rem;
  font-weight: 700;
}
.stat-note {
  color: #60747c;
  font-size: 0.78rem;
}
</style>
