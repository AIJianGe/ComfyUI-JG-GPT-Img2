import { app } from "../../scripts/app.js";

const DYNAMIC_NODES = [
    "GPT_Image_2_异步",
    "GPT_Image_2_综合",
    "GPT_Image_2_官方稳定版",
    "GPT_Image_2_官方4K",
    "GPT_智能对话",
];
const REF_INPUT_PREFIX = "🖼️ 参考图";
const COUNT_WIDGET_NAME = "🖼️ 参考图数量";
const MAX_REF = 20;

function updateRefInputs(node, count) {
    count = Math.max(1, Math.min(MAX_REF, parseInt(count) || 1));

    const existingRefs = [];
    for (let i = 0; i < node.inputs.length; i++) {
        const inp = node.inputs[i];
        if (inp && inp.name && inp.name.startsWith(REF_INPUT_PREFIX)) {
            const num = parseInt(inp.name.substring(REF_INPUT_PREFIX.length));
            if (!isNaN(num)) {
                existingRefs.push({ index: i, num: num });
            }
        }
    }
    const maxExisting = existingRefs.length > 0 ? Math.max(...existingRefs.map(r => r.num)) : 0;

    if (maxExisting > count) {
        for (let n = maxExisting; n > count; n--) {
            const name = `${REF_INPUT_PREFIX}${n}`;
            for (let i = node.inputs.length - 1; i >= 0; i--) {
                if (node.inputs[i] && node.inputs[i].name === name) {
                    node.removeInput(i);
                    break;
                }
            }
        }
    }

    if (maxExisting < count) {
        for (let i = maxExisting + 1; i <= count; i++) {
            node.addInput(`${REF_INPUT_PREFIX}${i}`, "IMAGE");
        }
    }

}

function setupDynamicRefInputs(node) {
    const countWidget = node.widgets?.find(w => w.name === COUNT_WIDGET_NAME);
    if (!countWidget) return;

    const origCallback = countWidget.callback;
    countWidget.callback = function (value) {
        origCallback?.call(this, value);
        updateRefInputs(node, value);
    };

    if (countWidget.inputEl) {
        countWidget.inputEl.addEventListener("change", () => {
            updateRefInputs(node, countWidget.inputEl.value);
        });
    }

    for (const w of node.widgets || []) {
        if (w.type === "customtext" || (w.inputEl && w.inputEl.tagName === "TEXTAREA")) {
            w.inputEl.style.height = "6em";
            w.inputEl.style.minHeight = "6em";
            w.inputEl.style.resize = "vertical";
        }
    }

    node._jg_updateRefInputs = updateRefInputs;
    node._jg_initTimer = setTimeout(() => {
        updateRefInputs(node, countWidget.value);
    }, 200);
}

app.registerExtension({
    name: "JG.DynamicRefInputs",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (!DYNAMIC_NODES.includes(nodeData.name)) return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);
            setupDynamicRefInputs(this);
        };

        const onConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function (config) {
            onConfigure?.apply(this, arguments);
            if (this._jg_initTimer) {
                clearTimeout(this._jg_initTimer);
                this._jg_initTimer = null;
            }
            const countWidget = this.widgets?.find(w => w.name === COUNT_WIDGET_NAME);
            if (countWidget) {
                setTimeout(() => updateRefInputs(this, countWidget.value), 50);
            }
        };
    }
});
