<template>
      <div class="page-about">
            <a-typography-title class="page-about-title">{{ $t("aboutPage.title") }}</a-typography-title>
            <a-row>
                  <a-col :span="12">
                        <img :src="require('../assets/images/illustration-woman-online-desktop.svg')" alt="Illustration" />
                        <img :src="require('../assets/images/illustration-box-desktop.svg')" alt="Illustration 2" />
                  </a-col>
                  <a-col :span="12">
                        <a-collapse v-model:activeKey="activeKey" expandIconPosition="right" :bordered="false" :style="{background: '#fff'}" accordion>
                              <a-collapse-panel :key="t.id" v-for="(t) in text" :header="t.title">
                                    <p>{{ t.text }}</p>
                              </a-collapse-panel>
                        </a-collapse>
                  </a-col>
            </a-row>


      </div>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
      const activeKey = ref(['1'])
      const text = ref([
            {
                  id: 1,
                  text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidid',
                  title: 'How many team members can I invite?',
            },
            {
                  id: 2,
                  text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidid',
                  title: 'What is the maximum file upload size?',
            },
            {
                  id: 3,
                  text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidid',
                  title: 'How do I reset my password?',
            },
            {
                  id: 4,
                  text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidid',
                  title: 'Can I cancel my subscription?',
            },
            {
                  id: 5,
                  text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidid.',
                  title: 'Do you provide additional support?',
            }
      ])
      const customStyle =
      'background: #fff;';

      return {
        activeKey,
        text,
        customStyle
      }
  }
});
</script>

<style lang="scss">
.page-about-title {
      font-family: var(--primary-font-bold);
}

.ant-collapse-item-active .ant-collapse-header {
      font-family: var(--primary-font-bold);
}

@media screen and (max-width: 375px) {
      .page-about img {
            display: none;
      }
}
</style>
