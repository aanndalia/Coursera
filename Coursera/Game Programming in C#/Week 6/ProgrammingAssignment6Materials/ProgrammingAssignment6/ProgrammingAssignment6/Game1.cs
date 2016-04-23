using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Audio;
using Microsoft.Xna.Framework.Content;
using Microsoft.Xna.Framework.GamerServices;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Microsoft.Xna.Framework.Media;

using XnaCards;

namespace ProgrammingAssignment6
{
    /// <summary>
    /// This is the main type for your game
    /// </summary>
    public class Game1 : Microsoft.Xna.Framework.Game
    {
        GraphicsDeviceManager graphics;
        SpriteBatch spriteBatch;
        
        // keep track of game state and current winner
        static GameState gameState = GameState.Play;
        Player currentWinner = Player.None;
        Deck deck;
        GameState lastGameState = GameState.Play;

        // hands and battle piles for the players
        WarHand player1_hand;
        WarHand player2_hand;
        WarBattlePile player1_pile;
        WarBattlePile player2_pile;

        // winner messages for players
        WinnerMessage player1_winmessage;
        WinnerMessage player2_winmessage;

        // menu buttons
        MenuButton collectButton;
        MenuButton flipButton;
        MenuButton quitButton;

        // set constants for window resolution and deck
        const int WINDOW_WIDTH = 800;
        const int WINDOW_HEIGHT = 600;
        const int CARDS_IN_DECK = 52;
 
        public Game1()
        {
            graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";

            // make mouse visible and set resolution
            graphics.PreferredBackBufferWidth = WINDOW_WIDTH;
            graphics.PreferredBackBufferHeight = WINDOW_HEIGHT;

            this.IsMouseVisible = true;
        }

        /// <summary>
        /// Allows the game to perform any initialization it needs to before starting to run.
        /// This is where it can query for any required services and load any non-graphic
        /// related content.  Calling base.Initialize will enumerate through any components
        /// and initialize them as well.
        /// </summary>
        protected override void Initialize()
        {
            // TODO: Add your initialization logic here

            base.Initialize();
        }

        /// <summary>
        /// LoadContent will be called once per game and is the place to load
        /// all of your content.
        /// </summary>
        protected override void LoadContent()
        {
            // Create a new SpriteBatch, which can be used to draw textures.
            spriteBatch = new SpriteBatch(GraphicsDevice);

            // create the deck object and shuffle
            deck = new Deck(Content, 100, 100);
            deck.Shuffle();

            // create the player hands and fully deal the deck into the hands
            player1_hand = new WarHand(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3 / 4);
            player2_hand = new WarHand(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 1 / 4);
            for (int i = 0; i < /*CARDS_IN_DECK / */2; i++)
            {
                player1_hand.AddCard(deck.TakeTopCard());
                player2_hand.AddCard(deck.TakeTopCard());
            }
            
            // create the player battle piles
            player1_pile = new WarBattlePile(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3 / 4 - 100);
            player2_pile = new WarBattlePile(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 1 / 4 + 100);

            // create the player winner messages
            player1_winmessage = new WinnerMessage(Content, WINDOW_WIDTH / 2 + player1_hand.Width + 100, WINDOW_HEIGHT * 3 / 4);
            player2_winmessage = new WinnerMessage(Content, WINDOW_WIDTH / 2 + player2_hand.Width + 100, WINDOW_HEIGHT * 1 / 4);

            // create the menu buttons
            flipButton = new MenuButton(Content, "flipbutton", 150, WINDOW_HEIGHT * 1 / 4, GameState.Flip);
            quitButton = new MenuButton(Content, "quitbutton", 150, WINDOW_HEIGHT * 3 / 4, GameState.Quit);
            collectButton = new MenuButton(Content, "collectwinningsbutton", 150, WINDOW_HEIGHT / 2, GameState.CollectWinnings);

            // initially do not show collect winnings button
            collectButton.Visible = false;
        }

        /// <summary>
        /// UnloadContent will be called once per game and is the place to unload
        /// all content.
        /// </summary>
        protected override void UnloadContent()
        {
            // TODO: Unload any non ContentManager content here
        }

        /// <summary>
        /// Allows the game to run logic such as updating the world,
        /// checking for collisions, gathering input, and playing audio.
        /// </summary>
        /// <param name="gameTime">Provides a snapshot of timing values.</param>
        protected override void Update(GameTime gameTime)
        {
            // Allows the game to exit
            if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed)
                this.Exit();

            // update the menu buttons
            MouseState currentMouseState = Mouse.GetState();
            collectButton.Update(currentMouseState);
            flipButton.Update(currentMouseState);
            quitButton.Update(currentMouseState);
 
            // update based on game state
            // Handle action updates only if game state changed since last frame
            if (gameState != lastGameState)
            {
                if (gameState == GameState.Play)
                {
                    // show Flip button and hide Collect Winnings button
                    flipButton.Visible = true;
                    collectButton.Visible = false;
                }
                else if (gameState == GameState.CollectWinnings)
                {
                    // add the cards from both battle piles to the hand of the player who had the highest card
                    // also make winner message disappear
                    if (currentWinner == Player.Player1)
                    {
                        player1_hand.AddCards(player1_pile);
                        player1_hand.AddCards(player2_pile);
                        player1_winmessage.Visible = false;

                    }
                    else if (currentWinner == Player.Player2)
                    {
                        player2_hand.AddCards(player1_pile);
                        player2_hand.AddCards(player2_pile);
                        player2_winmessage.Visible = false;
                    }
                    else
                    {
                        // In the case of a tie
                        // add Player 1’s battle pile to Player 1’s hand and Player 2’s battle pile to Player 2’s hand
                        player1_hand.AddCards(player1_pile);
                        player2_hand.AddCards(player2_pile);
                    }

                    // collect winnings button should disappear and the flip button should appear
                    collectButton.Visible = false;
                    flipButton.Visible = true;

                    // If one of the player’s hands is empty after the collect winnings button has been clicked, the game is over                      
                    if (player1_hand.Empty || player2_hand.Empty)
                    {
                        gameState = GameState.GameOver;
                    }

                }
                else if (gameState == GameState.Flip)
                {
                    // remove a card from the Player 1 hand, flip it over, and add it to the Player 1 battle pile
                    Card p1_topCard = player1_hand.TakeTopCard();
                    p1_topCard.FlipOver();
                    player1_pile.AddCard(p1_topCard);

                    // do the above steps for Player 2 as well
                    Card p2_topCard = player2_hand.TakeTopCard();
                    p2_topCard.FlipOver();
                    player2_pile.AddCard(p2_topCard);

                    // make the flip button invisible and make the collect winnings button visible
                    flipButton.Visible = false;
                    collectButton.Visible = true;

                    // figure out which player is the winner and display the Winner message
                    if (p1_topCard.WarValue > p2_topCard.WarValue)
                    {
                        currentWinner = Player.Player1;
                        player1_winmessage.Visible = true;
                    }
                    else if (p1_topCard.WarValue < p2_topCard.WarValue)
                    {
                        currentWinner = Player.Player2;
                        player2_winmessage.Visible = true;
                    }
                    else
                    {
                        // It's a tie!
                        currentWinner = Player.None;
                    }
                }
                
            }

            // Handle End of Game Conditions (Quit and Game Over)
            if (gameState == GameState.GameOver)
            {
                // Make flip button invisible in this case. 
                // Also display the winner message next to the winning player’s hand.
                flipButton.Visible = false;

                if (currentWinner == Player.Player1)
                    player1_winmessage.Visible = true;
                else
                    player2_winmessage.Visible = true;

            }
            else if (gameState == GameState.Quit)
            {
                // Game state must be Quit
                Exit();
            }

            // Set previous game state so we only update once per changed state
            lastGameState = gameState;

            base.Update(gameTime);
        }

        /// <summary>
        /// This is called when the game should draw itself.
        /// </summary>
        /// <param name="gameTime">Provides a snapshot of timing values.</param>
        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.Goldenrod);
            spriteBatch.Begin();

            // draw the game objects
            player1_hand.Draw(spriteBatch);
            player2_hand.Draw(spriteBatch);
            player1_pile.Draw(spriteBatch);
            player2_pile.Draw(spriteBatch);

            // draw the winner messages
            player1_winmessage.Draw(spriteBatch);
            player2_winmessage.Draw(spriteBatch);

            // draw the menu buttons
            collectButton.Draw(spriteBatch);
            flipButton.Draw(spriteBatch);
            quitButton.Draw(spriteBatch);

            spriteBatch.End();
            base.Draw(gameTime);
        }

        /// <summary>
        /// Changes the state of the game
        /// </summary>
        /// <param name="newState">the new game state</param>
        public static void ChangeState(GameState newState)
        {
            gameState = newState;
        }
    }
}
