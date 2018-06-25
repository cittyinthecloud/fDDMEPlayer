var menu = [{
        name: 'Delete Mod',
        title: 'Delete Mod',
        fun: function (data, event) {
            var modid = data.trigger.attr("modid")
            if(modid == "vanilla"){
                alert("Can you don't?")
            } else {
                if(window.confirm("Are you sure you want to delete this mod ("+modid+")")){
                    $.get("/api/"+modid+"/delete",function(){
                        console.log("Launched mod.")
                    })
                }
            }
        }}];
$(document).ready(function(){
    $(".launchButton").contextMenu(menu,{triggerOn:"contextmenu",mouseClick:"right"})
    $(".launchButton").click(function (event){
        var modid = $(this).attr("modid")
        $.get("/api/"+modid+"/launch",function(){
            console.log("Launched mod.")
        })
        event.preventDefault()
    })
});
