const img = document.getElementById("img");
const cam = document.getElementById("cam");

let loading = false;

setInterval(() => {
    if (loading) return;

    loading = true;

    img.src = "/frame?" + Date.now();

    img.onload = () => {
        loading = false;
    };
}, 125);

cam.onchange = async () => {
    try {
        let r = await fetch("/camera", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                camera_index: cam.value
            })
        });

        let data = await r.json();

        if (data.status !== "ok") {
            alert("Camera gagal dibuka!");
        }

    } catch (e) {
        alert("Error koneksi ke server camera!");
        console.log(e);
    }
};

setInterval(async()=>{
    try {
        let r = await fetch("/stats");
        if(!r.ok) return;

        let j = await r.json();

        document.getElementById("stats").innerHTML =
        "FPS: "+j.fps+" | Frames: "+j.frames_served+" | Camera: "+j.camera;

    } catch(e){
        console.log("stats error", e);
    }
},1000);