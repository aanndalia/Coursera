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

namespace GameProject
{
    /// <summary>
    /// This is the main type for your game
    /// </summary>
    public class Game1 : Microsoft.Xna.Framework.Game
    {
        GraphicsDeviceManager graphics;
        SpriteBatch spriteBatch;

        // game state
        GameState gameState = GameState.Menu;

        // Increment 1: opening screen fields
        Texture2D openingScreenTexture; // The opening screen texture
        Rectangle openingScreenRectangle; // The opening screen rectangle

        // Increment 2: the board
        NumberBoard numberBoard;

        // Create random generator field
        Random rand = new Random();

        // Audio objects
        AudioEngine engine;
        SoundBank soundBank;
        WaveBank waveBank;

        public Game1()
        {
            graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";

            // Increment 1: set window resolution
            // Setting window resolution to 800 by 600
            graphics.PreferredBackBufferWidth = 800;
            graphics.PreferredBackBufferHeight = 600;

            // Increment 1: make the mouse visible
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

            // Increment 1: load opening screen and set opening screen draw rectangle
            // Set the opening screen to take up the entire window
            openingScreenRectangle = new Rectangle(0, 0, graphics.PreferredBackBufferWidth, graphics.PreferredBackBufferHeight);

            // Load the opening screen texture
            openingScreenTexture = Content.Load<Texture2D>("openingscreen");

            // load audio content
            engine = new AudioEngine(@"Content\sounds.xgs");
            soundBank = new SoundBank(engine, @"Content\Sound Bank.xsb");
            waveBank = new WaveBank(engine, @"Content\Wave Bank.xwb");

            StartGame();
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
            // Allows the game to exit on keyboard Escape
            KeyboardState keyboardState = Keyboard.GetState();
            if (keyboardState.IsKeyDown(Keys.Escape))
                this.Exit();

            // Increment 2: change game state if game state is GameState.Menu and user presses Enter
            if ((gameState == GameState.Menu) && Keyboard.GetState().IsKeyDown(Keys.Enter))
            {
                gameState = GameState.Play;
            }
            else if (gameState == GameState.Play)
            {
                // if we're actually playing, update mouse state and update board
                MouseState currentMouseState = Mouse.GetState();
                bool correctGuess = numberBoard.Update(gameTime, currentMouseState);

                // restart the game if a correct guess was chosen
                if (correctGuess)
                {
                    soundBank.PlayCue("newGame");
                    StartGame();
                }
            }

            base.Update(gameTime);
        }

        /// <summary>
        /// This is called when the game should draw itself.
        /// </summary>
        /// <param name="gameTime">Provides a snapshot of timing values.</param>
        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.CornflowerBlue);

            // Increments 1 and 2: draw appropriate items here
            spriteBatch.Begin();

            if (gameState == GameState.Menu)
            {
                // Draw opening screen texture
                spriteBatch.Draw(openingScreenTexture, openingScreenRectangle, Color.White);
            }

            else if (gameState == GameState.Play)
            {
                numberBoard.Draw(spriteBatch);
            }

            spriteBatch.End();

            base.Draw(gameTime);
        }

        /// <summary>
        /// Starts a game
        /// </summary>
        void StartGame()
        {
            // randomly generate new number for game
            int correctNumber = rand.Next(1, 10);

            // Increment 2: create the board object (this will be moved before you're done with the project)
            // Set center point
            float centerX = graphics.PreferredBackBufferWidth / 2.0f;
            float centerY = graphics.PreferredBackBufferHeight / 2.0f;
            Vector2 center = new Vector2(centerX, centerY);

            // Set board length less than height of window
            int boardLength = graphics.PreferredBackBufferHeight - 100;
            numberBoard = new NumberBoard(Content, center, boardLength, correctNumber, soundBank);

        }
    }
}
