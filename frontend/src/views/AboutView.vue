<template>
      <div class="page-about">
            <h1>About Invoices CMS</h1>

            <p>Hosted by Azure App Service / Azure Flexible SQL server</p>

            <a-collapse v-model:activeKey="activeKey" accordion>
                  <a-collapse-panel key="1" header="This is panel header 1">
                        <p>{{ text }}</p>
                  </a-collapse-panel>
                  <a-collapse-panel key="2" header="This is panel header 2" :disabled="false">
                        <p>{{ text }}</p>
                  </a-collapse-panel>
                  <a-collapse-panel key="3" header="How">
                        <p>{{ text }}</p>
                  </a-collapse-panel>
            </a-collapse>
      </div>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
      const activeKey = ref([])
      const text = ref('This is panel header 1')

      return {
        activeKey,
        text
      }
  }
});
</script>
