class Game {
    constructor({
        boardElement = document.getElementById("board"),
        tiles = [],
        rows = 4,
        columns = 4,
        boardData = []
        
        } = {}) {
        this.board = {
            gameBoard: boardElement,
            isShuffled: false,
        };
        this.tiles = tiles;
        this.boardData = boardData
        this.winningTiles = Array.from({ length: rows * columns }, (_, i) => (i + 1 === rows * columns ? null : i + 1));;
        this.winner = false;
        this.rows = rows;
        this.columns = columns;
        this.init();
    }

    init() {
        // Clear the board container in case of reinitialization
        this.board.gameBoard.innerHTML = "";

        let index = 0;
        for (let i = 0; i < this.rows; i++) {
            let row = document.createElement("div");
            row.className = "row";

            for (let j = 0; j < this.columns; j++) {
                let cell = document.createElement("div");
                let value = this.boardData[index];

                cell.className = "tile";
                cell.dataset.index = index + 1; // Index starts at 1
                cell.dataset.value = value === null ? "16" : value; // Empty cell as "16"
                cell.textContent = value === null ? "" : value;

                row.appendChild(cell);
                this.tiles.push(cell); // Store tile reference
                index++;
            }
            this.board.gameBoard.appendChild(row);
        }

        this.tiles.forEach((tile) => {
            tile.addEventListener("click", (event) => {
                if (!this.winner) {
                    this.click(event);
                }
            });
        });

        this.board.isShuffled = true; // Assume boardData is already shuffled
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

        if (this.board.isShuffled) {
            this.checkWin();
        }
    }

    swap(i, j) {
        let temp = this.tiles[i].dataset.value;
        this.tiles[i].textContent = this.tiles[j].textContent;
        this.tiles[i].dataset.value = this.tiles[j].dataset.value;
        this.tiles[j].textContent = temp === "0" ? "" : temp;
        this.tiles[j].dataset.value = temp;
    }

    checkWin() {
        for (let i = 0; i < this.tiles.length; i++) {
            if (this.tiles[i].dataset.value != this.winningTiles[i]) {
                console.log("Not yet");
                return;
            }
        }
        console.log("you win");
        this.winner = true;
        this.tiles[this.tiles.length - 1].textContent = "16";
    }
}

// Instantiate Game once DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    const game = new Game({
        boardData: boardData // Use the globally available boardData from Flask
    });
});
