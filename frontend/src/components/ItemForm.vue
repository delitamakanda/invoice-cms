<template>
    <div>
        <a-form-item ref="title" label="Title" name="title">
            <a-input v-model:value="formState.item.title" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="unit_price" label="Price" name="unit_price">
            <a-input v-model:value="formState.item.unit_price" type="number" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="quantity" label="Quantity" name="quantity">
            <a-input v-model:value="formState.item.quantity" type="number" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="vat_rat" label="VAT Rate" name="vat_rate">
            <a-select v-model:value="formState.item.vat_rate" style="width: 120px" :options="options"></a-select>
        </a-form-item>
        <a-form-item ref="gross_amount" label="Gross amount" name="gross_amount">
            <a-input v-model:value="gross_amount" type="text"  disabled placeholder="input placeholder" />
        </a-form-item>
        
    </div>
</template>

<script>
import { defineComponent, reactive, computed, ref, toRaw } from 'vue'

const options = ref([
    {
        value: '0',
        label: '0%',
    },
    {
        value: '5',
        label: '5%',
    },
    {
        value: '14',
        label: '14%',
    },
    {
        value: '20',
        label: '20%',
    },
    {
        value: '25',
        label: '25%',
    }
]);

export default defineComponent({
    setup(props, context) {
        const formRef = ref()
        const formState = reactive({
            item: props.initialItem
        })

        const rules = {
            title: [
                {
                    required: true,
                    message: 'Please input Title',
                    trigger: 'blur',
                }
            ],
            unit_price: [
                {
                    required: true,
                    message: 'Please input Price',
                    trigger: 'blur',
                }
            ],
            quantity: [
                {
                    required: true,
                    message: 'Please input Quantity',
                    trigger: 'blur',
                }
            ],
            vat_rate: [
                {
                    required: true,
                    message: 'Please input VAT rate',
                    trigger: 'change',
                }
            ]
        }

        const gross_amount = computed({
            get() {
                const unit_price = formState.item.unit_price
                const quantity = formState.item.quantity
                const vat_rate = formState.item.vat_rate

                formState.item.net_amount = unit_price * quantity

                context.emit('updatePrice', formState.item)

                return formState.item.net_amount + (formState.item.net_amount * (vat_rate / 100))
            },
            set(value) {
            }
        });

        return {
            formRef,
            formState,
            rules,
            options,
            gross_amount,
        }
    },
    props: {
        initialItem: Object
    }
})
</script>

<style>

</style>