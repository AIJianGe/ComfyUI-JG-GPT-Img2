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
const MAX_REF = 4;

function updateRefInputs(node, count) {
    count = Math.max(1, Math.min(MAX_REF, parseInt(count) || 1));

    for (let i = node.inputs.length - 1; i >= 0; i--) {
        if (node.inputs[i] && node.inputs[i].name && node.inputs[i].name.startsWith(REF_INPUT_PREFIX)) {
            node.removeInput(i);
        }
    }

    for (let i = 1; i <= count; i++) {
        node.addInput(`${REF_INPUT_PREFIX}${i}`, "IMAGE");
    }

    const sz = node.computeSize();
    if (sz[0] < node.size[0]) sz[0] = node.size[0];
    if (sz[1] < node.size[1]) sz[1] = node.size[1];
    node.setSize(sz);
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
