
# FarmBOT - Automation of the "Wolni Farmerzy" game

FarmBOT is an application that allows for the automatic execution of actions in the Wolni Farmerzy game.

## List of contents
1. [Project description](#project-description)
2. [Environment Variables](#environment-variables)
3. [Run Locally](#run-locally)
4. [Supported crops and their seeds](#supported-crops-and-their-seeds)
5. [Roadmap](#roadmap)
6. [Screenshots](#roadmap)

## Project description
The aim of the project was to create a bot that would handle essential game functions in Wolni Farmerzy, such as harvesting crops from all gardens, planting selected crops, watering plants, collecting animal products, and feeding animals. These tasks are time-consuming due to the game's unoptimized interface. The development of this bot was initiated at the request of a friend who found these tasks to be particularly cumbersome. The bot leverages FastAPI (though it is not mandatory) for the purpose of running it on a server, ensuring uninterrupted operation.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`NICKNAME: Your username`

`PASSWORD: Your password`

`SERVER: Your account's server`

`PHPSESSID: PHP session cookie`

`SEED: id of the plant to be planted`

## Run Locally

Clone the project

```bash
git clone https://github.com/Crapteep/FarmBOT
```

Go to the project directory

```bash
cd FarmBOT
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the server

```bash
uvicorn main:app --reload
```

The bot will initiate its operations upon startup. The bot will be running on port 8000. You can now access the API interface at: http://localhost:8000
## Supported crops and their seeds.


| Type       | Seed |
| :--------- | :--- |
| Wheat      | 1    |
| Corn       | 2    |
| Clover     | 3    |
| Rapeseed   | 4    |
| Sugar Beets| 5    |
| Herbs      | 6    |
| Sunflower  | 7    |
| Bachelor's Buttons | 8    |
| Carrot     | 17   |
| Cucumber   | 18   |
| Radish     | 19   |
| Strawberry | 20   |
| Tomato     | 21   |
| Onion      | 22   |
| Spinach    | 23   |
| Cauliflower| 24   |
| Potato     | 26   |
| Asparagus  | 29   |
| Zucchini   | 31   |
| Berries    | 32   |
| Raspberries| 33   |
| Currants   | 34   |
|Blackberries| 35   |
| Mirabelles | 36   |
| Thistles   | 108  |
| Daisies    | 109  |
| Tea        | 129  |


## Roadmap

- Adding market/customer service

- Adding support for additional farms (I don't have access to them yet)
- Creating a website to manage bot settings
- Notification handling in case of error
- Adding a change in the bot's functionality that enables the independent activation of each farm as soon as it's completed, rather than waiting for a fixed 10-minute interval
- At this point, harvesting is only possible with the "Harvest All" function available in the game
## Screenshots

![Startup Farm](https://github.com/Crapteep/FarmBOT/blob/master/screenshots/startup_f.png)

