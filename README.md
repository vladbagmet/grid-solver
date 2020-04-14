# Grid Solver
Simple service to solve grids in automated mode.
HTTP service is also available in case you want to try out your own grid solver.


## Prerequisites
* Installed Python 3.6+ interpreter
* Activated new virtual environment
* Git client

## Installation
* Clone repository `https://gitlab.com/b77mail/grid-solver.git`
* `cd grid-solver`
* Install external dependencies `pip install -r requirements.txt`

## Running Code Checks
* Run `make test` to launch tests
* Run `make check` to launch code quality checks (Flake8 is used)

## Launching HTTP Service (API)
* Specify Flask app path `export FLASK_APP=handlers/web.py:app`
* Launch HTTP server `flask run`

At this point server should be available by url `http://127.0.0.1:5000/`

## API Manipulations
To solve grids in a programmatic way, there are 2 endpoints available.
Before sending any HTTP requests, please make sure to set headers.
Allowed `Content-Type` is `application/json`.

* `/mine_field` - to create new grid and be able to interact with it on the other endpoint    
    ```
    Accepted method: `POST`

    Inputs (should be passed in json payload):
        * `horizontalFieldSize` - Horizontal size of the mine field. Can be any positive number.
        * `verticalFieldSize` - Vertical size of the mine field. Can be any positive number.
        * `mines` - Number of mines to set on the field. Can be any positive number.
        * `discoverableRadius` - Distance from the current cell where nearest mine cells are looked for.
        * `openedCells` - Cells to open on the mine field before game starts.
    
    Outputs:
        * `mineFieldId` - id of the generated grid.
        * `gameState` - indicates the state of the game after the last interaction.
        * `mineField` - grid representation (example is given below).
        * `message` - result of last operation.
    
    Game state example:
    {
        "x_0^y_0": "?",
        "x_0^y_1": "?",
        "x_0^y_2": 2,
        "x_1^y_0": "?",
        "x_1^y_1": "?",
        "x_1^y_2": 2,
        "x_2^y_0": "?",
        "x_2^y_1": 2,
        "x_2^y_2": "?"
    }
    Record "x_0^y_0": "?" represents unknown cell(cell available for further discovery) with coordinates x=0 and y=0.
    ```
    
    New grid generation request example using CURL:
    ```
    curl -d '{
        "discoverableRadius": 2,
        "horizontalFieldSize": 3,
        "mines": 1,
        "openedCells": 3,
        "verticalFieldSize": 3
    }' -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/mine_field/
    ```
    
* `/mine_field/<mine_field_id>` - to discover generated grid cell by cell
    ```
    Accepted method: `PUT`
    
    URL Inputs:
        * `<mine_field_id>` - should be replaced with id of the generated grid obtained on previous endpoint.
        
    Request Body Inputs:
        * `x` - Cell x-axis coordinate to discover.
        * `y` - Cell y-axis coordinate to discover.
        
    Ouputs:
        * `mineFieldId`
        * `gameState`
        * `mineField`
        * `message`
        
    To solve the grid, please make 1 request for each cell you would like to discover.
    Manipulations with this enpoint are possible while `gameState` is `in progress`. 
    Once grid will be solved, `gameState` will be changed to `won` or `lost`.
    ```

    Solving existing grid  request example using CURL:
    ```
    curl -d '{
        "x": 0,
        "y": 0
    }' -X PUT -H "Content-Type: application/json" http://127.0.0.1:5000/mine_field/<mine_field_id>
    ```
    `<mine_field_id>` should be replaced by `mine_field_id` value which was received in response for new grid creation.

## Automatic Grid Solver Statistics
500k automated game rounds were played to get some initial data about how good is automatic solving.
```
Game settings common for all games:
    * horizontal_size: 5
    * vertical_size: 5
    * discoverable_radius: 2
    * opened_cells: 5
    
    

| Mines on field | Games played  | Won   | Lost  | Won    |
|:--------------:|:-------------:|:-----:|:-----:|:------:|
| 5              | 100 000       | 1594  | 98406 | 1.59%  |
| 4              | 100 000       | 4180  | 95820 | 4.18%  |
| 3              | 100 000       | 10578 | 89422 | 10.58% |
| 2              | 100 000       | 21735 | 78265 | 21.74% |
| 1              | 100 000       | 29707 | 70293 | 29.71% |
```

## ToDo (aka Future Work)
* CLI tool to let humans play the game
