
get_parent_category()
get_child_category()
get_grand_child_category()

$("#parent_category").change(function(){
    $("#grand_child_category option:nth-child(n+1)").remove();
    $("#child_category option:nth-child(n+1)").remove();
    set_default_grand_child()
    set_default_child()
    get_child_category()
});

$("#child_category").change(function(){
    $("#grand_child_category option:nth-child(n+1)").remove();
    set_default_grand_child()
    get_grand_child_category()
});

function get_parent_category(){
    $.getJSON(
        "/get_parent_category",{
    },function(data){
        for(let category in data["data"]){
            let op = document.createElement("option");
            op.value = data["data"][category]["name"];
            op.text = data["data"][category]["name"];
            document.getElementById("parent_category").append(op);
        };
    });
};

function get_child_category(){
    $.getJSON("/get_child_category",{
        path:$("#parent_category option:selected").text()+"/",
        hierarchy:2
    },function(data){
        for(let category in data["data"]){
            let op = document.createElement("option");
            op.value = data["data"][category]["id"];
            op.text = data["data"][category]["name"];
            document.getElementById("child_category").append(op);
        };
    });
};


function get_grand_child_category(){
    $.getJSON("/get_child_category",{
        path:$("#parent_category option:selected").text()+"/"+$("#child_category option:selected").text()+"/",
        hierarchy:3
    },function(data){
        for(let category in data["data"]){
            let op = document.createElement("option");
            op.value = data["data"][category]["id"];
            op.text = data["data"][category]["name"];
            document.getElementById("grand_child_category").append(op);
        };
    });
};

function set_default_grand_child(){
    let op = document.createElement("option");
        op.value = "";
        op.text = "--grandChild--";
        document.getElementById("grand_child_category").append(op);
}

function set_default_child(){
    let op = document.createElement("option");
    op.value = "";
    op.text = "--childCategory--";
    document.getElementById("child_category").append(op);
}

