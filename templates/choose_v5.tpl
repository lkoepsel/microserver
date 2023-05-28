{% args led_state, leds%}
      <form action="" method="POST">

        <label ><strong>Choose LED(s):</strong></label>
        <label >
          <input type="checkbox" name="led" value="YELLOW" {{ led_state[0] }}>
          YELLOW
        </label>
        <label >
          <input type="checkbox" name="led" value="GREEN" {{ led_state[1] }}>
          GREEN
        </label>
        <label >
          <input type="checkbox" name="led" value="RED" {{ led_state[2] }}>
          RED
        </label>
        <label >
          <input type="checkbox" name="led" value="BLUE" {{ led_state[3] }}>
          BLUE
        </label>

        <div align="left">
          <input type="submit" value="Lights!">
        </div>

      </form>
