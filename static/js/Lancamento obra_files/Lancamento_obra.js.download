function toggleDiaria() {
    diaria = $("#".concat(objLoaded.prefix, "diaria"));
    if ($("#".concat(objLoaded.prefix, "contrato")).val() == "Terceiro") {
        diaria.attr("disabled", false);
    } else {
        diaria.attr("disabled", true);
        diaria.val("");
    }
}

function deleteData(id) {
    apiRequest.delete('deletar',objLoaded.name,id,function(){$("#table").bootstrapTable('refresh')})
}
// Preenche as variaveis de dados de objetos do banco de dados
var objLoaded = { method: undefined, name: undefined, prefix: undefined,
    field: function(id){
        return $(`#${prefix}_${id}`);
    }
,};
var columns = {
    inputs: undefined,
    checks: undefined,
    obj: undefined,
    select: undefined,
    
};
var modalLoad;
function changeAtividade() {
    let obra = $("#" + objLoaded.prefix + "obra_id").val();
    const campos1 = [
        "horaini3",
        "horafim3",
        "diaseguinte",
        "atividade_id",
    ];
    const campos2 = ["supervisor_id", "motivo"];
    if (obra > 1 && obra < 5) {
        desativado = true;
    } else {
        desativado = false;
    }
    for (let X in campos1) {
        $("#" + objLoaded.prefix + campos1[X]).attr("disabled", desativado);
    }
    for (let X in campos2) {
        $("#" + objLoaded.prefix + campos2[X]).attr("disabled", !desativado);
    }
}
function changeObra() {
    const att = ['ATESTADO', 'DISPENSA', 'FALTA', 'FOLGA', 'FÉRIAS', 'TREINAMENTO', 'ATIVIDADE OBRA']

    let obra = $("#" + objLoaded.prefix + "obra_id").val();
    if (obra >= 7) {
        $("#" + objLoaded.prefix + "atividade_id").val(att[6]);
    } else {
        $("#" + objLoaded.prefix + "atividade_id").val(att[obra - 1]);
    }
    changeAtividade();
}
function removeColumns(value) {
    if (value in columns.inputs) {
        columns.inputs.slice(columns.inputs.indexOf(value), 1);
    } else if (value in columns.checks) {
        columns.checks.slice(columns.checks.indexOf(value), 1);
    } else if (value in columns.select) {
        columns.select.slice(columns.select.indexOf(value), 1);
    }
}
function loadColumns(oculto) {
    if (objLoaded != columns.obj) {
        let inputs = [];
        let checks = [];
        let select = [];
        if (objLoaded.name === "atividade") {
            inputs = [
                "dia",
                "descricao",
                "indice",
                "horaini1",
                "horafim1",
                "horaini2",
                "horafim2",
                "horaini3",
                "horafim3",
                "motivo",
            ];
            checks = ["diaseguinte", "meiadiaria"];
            select = ["obra_id", "atividade_id", "colaborador", "supervisor_id"];
        } else if (objLoaded.name === "colaborador") {
            inputs = [
                "nome",
                "admissao",
                "contrato",
                "diaria",
                "observacao",
                "demissao",
            ];
            checks = ["encarregado"];
            select = ["funcao"];
        } else if (objLoaded.name === "obra") {
            inputs = [
                "id",
                "orcamento",
                "empresa",
                "cidade",
                "descricao",
                "indice",
                "retrabalho",
                'tecnicon',
            ];
            checks = ["finalizada"];
            select = ["supervisor_id"];
        } else if (objLoaded.name === "diario") {
            inputs = [
                "indice",
                "data",
                "climamanha",
                "climatarde",
                "descricao",
            ];
            select = ["encarregado", "obra_id"];
        } else if (objLoaded.name === "supervisor") {
            inputs = ["supervisor"];
            checks = ["ativo"];
        } else if (objLoaded.name === "funcao") {
            inputs = ["funcao", "grupo"];
        } else if (objLoaded.name === "programacao") {
            inputs = ["observacao", "iniciosemana"];
            select = ["colaborador", "encarregado", "obra_id"];
        }
        columns = {
            inputs: inputs,
            checks: checks,
            select: select,
            obj: objLoaded,
        };
        for (i = 0; i < columns.select.length; i++) {
            loadSelect(columns.select[i], oculto);
        }

    }
}
function getData(){
    data = {}
    values = columns.inputs.concat(columns.select)
    for (let i = 0; i < values.length; i++) {
        data[values[i]] = $("#" + objLoaded.prefix + values[i]).val() || NaN;
    }
    for (let i = 0; i < columns.checks.length; i++) {
        data[columns.checks[i]] = $(
            "#" + objLoaded.prefix + columns.checks[i]
        ).prop("checked");
    }
    return data
}
// Faz um post na API para registrar oque estiver nos inputs, normalmente referente a um formulário
submit = {
    post: function(type){
        apiRequest.post(type,objLoaded.name,getData(),function(){$("#table").bootstrapTable("refresh");})
    },
    update: function(type){
        apiRequest.update(type,objLoaded.name,getData(),function(){$("#table").bootstrapTable("refresh");})
    },
}
function loadForm(name) {
    objLoaded = { method: "form", name: name, prefix: "form_" + name + "_" };
    loadColumns('oculto');
    $("#" + objLoaded.prefix + "btn").click(function () {
        submit.post("register");
    });
}
function toggleOculto(campo) {
    let element;
    let filtrar;
    if (campo == "colaborador") {
        element = $("#mostrar_demitidos");
    } else if (campo == "obra_id") {
        element = $("#mostrar_finalizadas");
    }
    let text = element.text().split(" ");
    if (text[0] == "exibir") {
        filtrar = false;
        element.text("ocultar ".concat(text[1]));
    } else {
        filtrar = true;
        element.text("exibir ".concat(text[1]));
    }
    if (!filtrar) {
        loadSelect(campo, "exibir");
    } else {
        loadSelect(campo, "oculto");
    }
}

function loadTable() {
    apiRequest.get('get_table','table',objLoaded.name,function(data){
        $("#".concat(objLoaded.prefix + "table")).empty();
        for (let i = 0; i < data.length; i++) {
            let row = "<tr>";
            if (objLoaded.name == "funcao") {
                row += `<td>${data[i].funcao}</td>`;
                if (data[i].grupo != null) {
                    row += `<td>${data[i].grupo}</td>`;
                }
                row += `<td><img src="${icon}/trash.svg" class="btn-icon" onclick='deleteData("${data[i].id}"); setTimeout(function() {loadTable();},200)' style='background:lightcoral;'></td>`;
            } else if (objLoaded.name == "supervisor") {
                let checked;
                row += `<td>${data[i].supervisor}</td>`;
                checked = data[i].ativo ? "checked" : "";
                row += `<td><input class="form-check-input" type="checkbox" ${checked} onclick="toggleAtivo('${
                    data[i].supervisor
                }', ${!data[i].ativo})"></td>`;
                row += `<td><img src="${icon}/trash.svg" class="btn-icon" onclick='deleteData("${data[i].supervisor}"); setTimeout(function() {loadTable();},200)' style='background:lightcoral;'></td>`;
            } else {
                return alert("Nenhuma table encontrado");
            }
            row += "</tr>";
            $("#".concat(objLoaded.prefix + "table")).append(row);
        }
    })
}
function loadSelect(select, filter) {
    apiRequest.get('get_table','select',select,function(data){
        let selectHTML = objLoaded.prefix + select;
        $("#".concat(selectHTML)).empty();
        for (let i = 0; i < data.length; i++) {
            let value;
            let text;
            if (select == "funcao") {
                value = data[i].funcao;
            } else if (select == "obra_id") {
                if (filter == "oculto" && data[i].finalizada) {
                } else {
                    value = data[i].id;
                    text =
                        value +
                        " || " +
                        data[i].empresa +
                        " | " +
                        data[i].cidade;
                }
            } else if (select == "supervisor_id") {
                value = data[i].supervisor;
            } else if (select == "atividade_id") {
                value = data[i].tipo;
                // text = data[i].tipo;
            } else if (select == "colaborador") {
                if (filter == "oculto" && data[i].demissao != null) {
                } else {
                    value = data[i].nome;
                }
            } else if (select == "encarregado") {
                value = data[i].nome;
            } else {
                return alert("Nenhum select encontrado");
            }
            if (value != undefined) {
                let opt = document.createElement("option");
                opt.value = value;
                opt.text = text || value;
                $("#".concat(selectHTML)).append(opt);
            }
        }
    })
}


function previewModal_img(img) {
    image = document.getElementById("view_" + objLoaded.name + "_digitalizado");
    image.src = img;
}
