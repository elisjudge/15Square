class Game {
    constructor({
        board = document.getElementById("board"),
        tiles = [],
        rows = 4,
        columns = 4
        } = {}) {
        this.board = board;
        this.tiles = tiles;
        this.rows = rows;
        this.columns = columns;
        this.init();
    }

    init() {
        for (let i = 0; i < this.rows; i++) {
            let row = document.createElement("div");
            row.className = "row";
            for (let j = 0; j < this.columns; j++) {
                let cell = document.createElement("div");
                let index = i * 4 + j + 1;
                
                cell.className = "tile";

                cell.dataset.index = index;
                cell.dataset.value = index;
                cell.textContent = index === 16 ? "" : index;

                row.appendChild(cell);
                this.tiles.push(cell);  // Store tile reference
            }
            this.board.appendChild(row);
        }


        // Shuffle tiles 
        for (let i = 0; i < 1000; i++) {
            this.click({ 
                target: { 
                    dataset: {
                      index: Math.floor(Math.random() * 15) + 1   
                    }
                }
            });
        }


        this.tiles.forEach((tile) => {
            tile.addEventListener("click", (event) => {
                this.click(event);
            });
        });
    }

    click(e) {
        let i = parseInt(e.target.dataset.index, 10) - 1;

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
