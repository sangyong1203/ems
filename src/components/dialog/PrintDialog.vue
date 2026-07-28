<template>
    
    <el-dialog
        :model-value="modelValue"
        :title="title"
        style="height:210mm; overflow: hidden; margin-top: 5vh;"
        width="312mm"
    >
        <div class="print-dialog__body" id="printArea">
            <slot></slot>
        </div>

        <template #footer>
            <el-button type="primary" @click="makePdf">Download PDF</el-button>
            <el-button type="primary" v-print="print">Print</el-button>
            <el-button @click="closeDialog">Cancel</el-button>
        </template>
    </el-dialog>
        
</template>

<script setup lang="ts">

import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'

import { toRefs } from 'vue'
export interface Props {
    title: string
    modelValue: boolean
}
const props = defineProps<Props>()
const { title, modelValue } = toRefs(props)



const emit = defineEmits(['close'])
const closeDialog = (): void => {
    emit('close', false)
}

const print: any = {
    id: 'printArea',
    popTitle: '.',
    previewTitle: '',
    extraHead: '',
    zIndex: 20002,
    standard: '',
    extarCss: '',
    preview: false,
    previewPrintBtnLabel: 'Print',
}

const makePdf = ()=>{
      const pdfArea:any = document.querySelector('#printArea')
      html2canvas(pdfArea).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('l', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = pdf.internal.pageSize.getHeight();
        
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save('download.pdf')
      })
}

</script>

<style scoped>
.print-dialog__body{
    padding: 16px;
    width: 289mm;
}

</style>
