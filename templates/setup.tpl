      {% args leds%}
      <form action="" method="POST">

        <label ><strong>Enter LED Label and Pico Pin:</strong></label>
        <label for="pin1" > Enter Label and Pin: </label>
          <input type="text" id="pin1" name="color_1" required 
            minlength="4" maxlength="8" size="10">
          <input type="number" id="pin1" name="pin_1"
                 min="4" max="29">
        <label for="pin1" > Enter Label and Pin: </label>
          <input type="text" id="pin2" name="color_2" required 
            minlength="4" maxlength="8" size="10">
          <input type="number" id="pin2" name="pin_2"
                 min="4" max="29">
        <label for="pin1" > Enter Label and Pin: </label>
          <input type="text" id="pin3" name="color_3" required 
            minlength="4" maxlength="8" size="10">
          <input type="number" id="pin3" name="pin_3"
                 min="4" max="29">
        <label for="pin1" > Enter Label and Pin: </label>
          <input type="text" id="pin4" name="color_4" required 
            minlength="4" maxlength="8" size="10">
          <input type="number" id="pin4" name="pin_4"
                   min="4" max="29">

        <div align="left">
          <input type="submit" value="Setup">
        </div>

      </form>
