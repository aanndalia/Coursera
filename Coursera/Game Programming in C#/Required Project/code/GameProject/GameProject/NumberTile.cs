using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Audio;
using Microsoft.Xna.Framework.Content;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace GameProject
{
    /// <remarks>
    /// A number tile
    /// </remarks>
    class NumberTile
    {
        #region Fields

        // original length of each side of the tile
        int originalSideLength;

        // current length of each side (for shrinking)
        float currentSideLength;

        // whether or not this tile is the correct number
        bool isCorrectNumber;

        // The sound bank object
        SoundBank sb;

        // drawing support
        Texture2D texture;
        Rectangle drawRectangle;
        Rectangle sourceRectangle;

        // The blinking tile texture
        Texture2D blinkingTileTexture;

        // The current texture used (either original or blinking)
        Texture2D currentTexture;

        // blinking support
        const int TOTAL_BLINK_MILLISECONDS = 4000;
        int elapsedBlinkMilliseconds = 0;
        const int FRAME_BLINK_MILLISECONDS = 1000;
        int elapsedFrameMilliseconds = 0;

        // shrinking support
        const int TOTAL_SHRINK_MILLISECONDS = 4000;
        int elapsedShrinkMilliSeconds = 0;

        bool isTileVisible = true;
        bool isTileBlinking = false;
        bool isTileShrinking = false;

        bool clickStarted = false;
        bool buttonReleased = false;

        #endregion

        #region Constructors

        /// <summary>
        /// Constructor
        /// </summary>
        /// <param name="contentManager">the content manager</param>
        /// <param name="center">the center of the tile</param>
        /// <param name="sideLength">the side length for the tile</param>
        /// <param name="number">the number for the tile</param>
        /// <param name="correctNumber">the correct number</param>
        /// <param name="soundBank">the sound bank for playing cues</param>
        public NumberTile(ContentManager contentManager, Vector2 center, int sideLength,
            int number, int correctNumber, SoundBank soundBank)
        {
            // set original side length field
            currentSideLength = this.originalSideLength = sideLength;

            // set sound bank field
            sb = soundBank;

            // load content for the tile and create draw rectangle
            LoadContent(contentManager, number);
            drawRectangle = new Rectangle((int)center.X - sideLength / 2,
                 (int)center.Y - sideLength / 2, sideLength, sideLength);

            // set isCorrectNumber flag
            isCorrectNumber = number == correctNumber;
        }

        #endregion

        #region Public methods

        /// <summary>
        /// Updates the button to check for a button click
        /// </summary>
        /// <param name="gamepad">the current mouse state</param>
        public bool Update(GameTime gametime, MouseState mouse)
        {
            if (isTileBlinking)
            {
                // update amount of time spent blinking so far
                elapsedBlinkMilliseconds += gametime.ElapsedGameTime.Milliseconds;

                // if it's been blinking longer than the limit, set blinking and visible fields to false
                if (elapsedBlinkMilliseconds >= TOTAL_BLINK_MILLISECONDS)
                {
                    isTileBlinking = false;
                    isTileVisible = true;
                    return true;
                }

                // update amount of time in the current blink frame
                elapsedFrameMilliseconds += gametime.ElapsedGameTime.Milliseconds;

                // if it's been in the blinking frame longer than the limit, change to next frame of blinking
                if (elapsedFrameMilliseconds >= FRAME_BLINK_MILLISECONDS)
                {
                    // switch source rectangle between left and right blinking number images based on frame
                    if (sourceRectangle.X == 0)
                        sourceRectangle.X = currentTexture.Width / 2;
                    else
                        sourceRectangle.X = 0;

                    elapsedFrameMilliseconds = 0;
                }
            }            
            else if (isTileShrinking)
            {
                // check if tile is shrinking and calculate time spent
                elapsedShrinkMilliSeconds += gametime.ElapsedGameTime.Milliseconds;
                currentSideLength = originalSideLength *
                                    ((TOTAL_SHRINK_MILLISECONDS - elapsedShrinkMilliSeconds) / (float)TOTAL_SHRINK_MILLISECONDS);

                if (currentSideLength > 0.0f)
                {
                    // still shrinking - set width and height of tile to new length
                    drawRectangle.Width = (int)currentSideLength;
                    drawRectangle.Height = (int)currentSideLength;
                }
                else
                {
                    isTileVisible = false;
                }
            }
            else if (drawRectangle.Contains(mouse.X, mouse.Y)) // check for mouse over button
            {
                // highlight button
                sourceRectangle.X = texture.Width / 2;

                // check for click started on button
                if (mouse.LeftButton == ButtonState.Pressed &&
                    buttonReleased)
                {
                    clickStarted = true;
                    buttonReleased = false;
                }
                else if (mouse.LeftButton == ButtonState.Released)
                {
                    buttonReleased = true;

                    // if click finished on button, change game state
                    // If the player just clicked on the tile and the tile corresponds to the correct number, 
                    // set the tile is blinking field to true, otherwise set the tile is shrinking field to true
                    if (clickStarted)
                    {
                        if (isCorrectNumber)
                        {
                            isTileBlinking = true;
                            sb.PlayCue("correctGuess"); // play the applause cue when correct guess
                            currentTexture = blinkingTileTexture;
                            sourceRectangle.X = 0;
                        }
                        else
                        {
                            isTileShrinking = true;
                            sb.PlayCue("incorrectGuess"); // play the loser cure when incorrect guess
                        }

                        clickStarted = false;
                    }
                }
            }
            else
            {
                sourceRectangle.X = 0;

                // no clicking on this button
                clickStarted = false;
                buttonReleased = false;
            }

            return false;
        }

        /// <summary>
        /// Draws the number tile
        /// </summary>
        /// <param name="spriteBatch">the SpriteBatch to use for the drawing</param>
        public void Draw(SpriteBatch spriteBatch)
        {
            // draw the tile
            if(isTileVisible)
                spriteBatch.Draw(currentTexture, drawRectangle, sourceRectangle, Color.White);
        }

        #endregion

        #region Private methods

        /// <summary>
        /// Loads the content for the tile
        /// </summary>
        /// <param name="contentManager">the content manager</param>
        /// <param name="number">the tile number</param>
        private void LoadContent(ContentManager contentManager, int number)
        {
            // convert the number to a string
            string numberString = ConvertIntToString(number);

            // load content for the tile and set source rectangle
            texture = contentManager.Load<Texture2D>(numberString);
            sourceRectangle = new Rectangle(0, 0, texture.Width / 2, texture.Height);

            // load blinking tile texture
            blinkingTileTexture = contentManager.Load<Texture2D>("blinking" + numberString);

            // Set the current texture to initialize to the non-blinking texture
            currentTexture = texture;
        }

        /// <summary>
        /// Converts an integer to a string for the corresponding number
        /// </summary>
        /// <param name="number">the integer to convert</param>
        /// <returns>the string for the corresponding number</returns>
        private String ConvertIntToString(int number)
        {
            switch (number)
            {
                case 1:
                    return "one";
                case 2:
                    return "two";
                case 3:
                    return "three";
                case 4:
                    return "four";
                case 5:
                    return "five";
                case 6:
                    return "six";
                case 7:
                    return "seven";
                case 8:
                    return "eight";
                case 9:
                    return "nine";
                default:
                    throw new Exception("Unsupported number for number tile");
            }

        }

        #endregion
    }
}
