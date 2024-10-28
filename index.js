class Game {
    constructor({
        table = document.getElementById("table"),
        tiles = [],
        rows = 4,
        columns = 4
        } = {}) {
        this.table = table;
        this.tiles = tiles;
        this.rows = rows;
        this.columns = columns;
        this.init();
    }

    init() {
        this.table.innerHTML = "";  

        for (let i = 0; i < this.rows; i++) {
            let tr = document.createElement("tr");
            for (let j = 0; j < this.columns; j++) {
                let td = document.createElement("td");
                let index = i * 4 + j + 1;
                
                td.className = "tile";

                td.index = index;
                td.dataset.value = index;
                td.textContent = index === 16 ? "" : index;

                tr.appendChild(td);
                this.tiles.push(td);  // Store tile reference
            }
            this.table.appendChild(tr);
        }

        // Shuffle tiles 
        for (let i = 0; i < 1000; i++) {
            this.click({ srcElement: { index: Math.floor(Math.random() * 15) + 1 }});
        }

        this.tiles.forEach((tile) => {
            tile.addEventListener("click", (event) => {
                this.click(event);
            });
        });
    }

    click(e) {
        let i = e.srcElement.index - 1;

        if (i - 4 >= 0 && this.tiles[i - 4].dataset.value === "16") {
            this.swap(i, i - 4);
        } else if (i + 4 < 16 && this.tiles[i + 4].dataset.value === "16") {
            this.swap(i, i + 4);
        } else if (i % 4 !== 0 && this.tiles[i - 1].dataset.value === "16") {
            this.swap(i, i - 1);
        } else if (i % 4 !== 3 && this.tiles[i + 1].dataset.value === "16") {
            this.swap(i, i + 1);
        }
    }

    swap(i, j) {
        let temp = this.tiles[i].dataset.value;
        this.tiles[i].textContent = this.tiles[j].textContent;
        this.tiles[i].dataset.value = this.tiles[j].dataset.value;
        this.tiles[j].textContent = temp === "0" ? "" : temp;
        this.tiles[j].dataset.value = temp;
    }
}

// Instantiate Game once DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    const game = new Game();
});
