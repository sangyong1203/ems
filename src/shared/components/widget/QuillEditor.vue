<template>
    <div class="quill-component-container">
        <div ref="editorRef"></div>
    </div>
</template>

<script lang="ts" setup>
import Quill, { type Parchment } from 'quill'
import 'quill/dist/quill.snow.css'
import pretty from 'pretty'

import { onMounted, onUnmounted, ref, shallowRef, watch } from 'vue'

Quill.debug('error')

type QuillAttributor = Parchment.RegistryDefinition & {
    whitelist: string[]
}

type QuillWithHtmlEditor = InstanceType<typeof Quill> & {
    txtArea?: HTMLTextAreaElement
}

const editorRef = ref<HTMLDivElement | null>(null)
const quill = shallowRef<QuillWithHtmlEditor | null>(null)


class ByeByeUploader {
    upload() {}
}
Quill.register({ 'modules/uploader': ByeByeUploader }, true)


const Size = Quill.import('attributors/style/size') as QuillAttributor
Size.whitelist = ['10px', '12px', '14px', '16px', '18px', '24px', '32px']
Quill.register(Size, true)


const Font = Quill.import('attributors/style/font') as QuillAttributor
Font.whitelist = ['MalgunGothic', 'Dodum', 'Goolim', 'Arial', 'Roman', 'Sans-serif', 'Verdana']
Quill.register(Font, true)


const icons = Quill.import('ui/icons') as Record<string, string>
icons['showHtml'] =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M344-336 200-480l144-144 56 57-87 87 87 87-56 57Zm272 0-56-57 87-87-87-87 56-57 144 144-144 144ZM200-120q-33 0-56.5-23.5T120-200v-160h80v160h160v80H200Zm400 0v-80h160v-160h80v160q0 33-23.5 56.5T760-120H600ZM120-600v-160q0-33 23.5-56.5T200-840h160v80H200v160h-80Zm640 0v-160H600v-80h160q33 0 56.5 23.5T840-760v160h-80Z"/></svg>'

defineOptions({
    name: 'quill-editor-component',
})

const props = defineProps({
    content: String,
    insertImage: Array,
    deleteImage: Array,
    htmlEditButton: { type: Boolean, default: false },
    imageUploader: { type: Boolean, default: false },
    enable: { type: Boolean, default: true },
    placeholder: { type: String, default: 'Please input content' },
})

const emit = defineEmits(['update:content', 'update:insertImage', 'update:deleteImage'])


watch(
    () => props.content,
    newHtml => {
        if (quill.value && newHtml !== quill.value.root.innerHTML) {
            quill.value.root.innerHTML = newHtml || ''
        }
    },
)

onMounted(() => {
    if (!editorRef.value) return

    quill.value = new Quill(editorRef.value, {
        theme: 'snow',
        placeholder: props.enable ? props.placeholder : '',
        modules: {
            toolbar: {
                container: [
                    [
                        {
                            font: [
                                'MalgunGothic',
                                'Dodum',
                                'Goolim',
                                'Arial',
                                'Roman',
                                'Sans-serif',
                                'Verdana',
                            ],
                        },
                    ],
                    [{ size: ['10px', '12px', false, '16px', '18px', '24px', '32px'] }],
                    ['bold', 'italic', 'underline', 'strike', { color: [] }, { background: [] }],
                    [{ list: 'ordered' }, { list: 'bullet' }],
                    ['image'],
                    ['clean', 'showHtml'],
                ],
                handlers: {
                    showHtml: () => {
                        const editor = quill.value
                        const txtArea = editor?.txtArea
                        const editorContent = editor?.container.firstElementChild

                        if (!editor || !txtArea || !editorContent) return

                        if (txtArea.style.display === '') {
                            editorContent.innerHTML = txtArea.value.replace(/\n/g, '')
                        } else {
                            txtArea.value = pretty(editor.root.innerHTML)
                        }
                        txtArea.style.display = txtArea.style.display === 'none' ? '' : 'none'
                    },
                },
            },
        },
    })

    quill.value.enable(props.enable)
    quill.value.root.setAttribute('spellcheck', 'false')
    quill.value.root.innerHTML = props.content || ''

    const txtArea = document.createElement('textarea')
    txtArea.setAttribute('spellcheck', 'false')
    txtArea.style.cssText =
        'width: 100%;margin: 0px;padding:10px;line-height: 24px;position: absolute;top: 0;bottom: 0;border: none;display:none;resize: none;'

    const htmlEditor = quill.value.addContainer('ql-custom')
    htmlEditor.appendChild(txtArea)
    quill.value.txtArea = txtArea

    quill.value.on('text-change', () => {
        emit('update:content', fnc.getContents())
    })
})

onUnmounted(() => {
    quill.value = null
})

const fnc = {
    getContents() {
        return quill.value?.root.innerHTML || ''
    },
    setContents(html: string) {
        if (quill.value) {
            quill.value.root.innerHTML = html
        }
    },
}

defineExpose({
    getContents: fnc.getContents,
    setContents: fnc.setContents,
})
</script>

<style scoped>
.quill-component-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    border: 1px solid var(--common-component-border-color);
    background: var(--common-component-bg-color);
    color: var(--text-color--body);
    box-sizing: border-box;
    position: relative;
}

:deep(.ql-toolbar.ql-snow) {
    display: flex !important;
    flex-wrap: nowrap !important;
    flex-shrink: 0;
    border: none !important;
    border-bottom: 1px solid var(--common-component-border-color) !important;
    z-index: 10;
    position: relative;
    background: var(--surface-elevated-color);
    color: var(--text-color--body);
}

:deep(.ql-snow .ql-picker-options) {
    z-index: 20 !important;
    background-color: var(--surface-elevated-color);
    border: 1px solid var(--common-component-border-color);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

:deep(.ql-container.ql-snow) {
    flex: 1 !important;
    height: 0 !important;
    border: none !important;
    display: flex;
    flex-direction: column;
    z-index: 1;
}

:deep(.ql-editor) {
    flex: 1;
    overflow-y: auto;
    color: var(--text-color--primary);
    background: var(--common-control-bg-color);
}

:deep(.ql-editor.ql-blank::before) {
    color: var(--text-color--placeholder);
}

:deep(.ql-toolbar.ql-snow .ql-formats) {
    display: flex !important;
    flex-shrink: 0 !important;
    margin-right: 8px !important;
}

:deep(.ql-custom textarea) {
    height: 100% !important;
    width: 100% !important;
}
</style>
