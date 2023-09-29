{% args def_pins %}

{% for pin in def_pins %}
    <input type="text" id="{{ pin[0] }}" name="label" required
        minlength="3" maxlength="20" size="10" value="{{ pin[2] }}" >
    <input type="number" name="pin" list="defaultNumbers" value="{{ pin[1] }}" />
    <datalist id="defaultNumbers">
      <option value="4"></option>
      <option value="5"></option>
      <option value="6"></option>
      <option value="7"></option>
      <option value="9"></option>
      <option value="10"></option>
      <option value="11"></option>
      <option value="12"></option>
      <option value="14"></option>
      <option value="15"></option>
      <option value="16"></option>
      <option value="17"></option>
      <option value="19"></option>
      <option value="20"></option>
      <option value="21"></option>
      <option value="22"></option>
      <option value="24"></option>
      <option value="25"></option>
      <option value="26"></option>
      <option value="27"></option>
      <option value="29"></option>
    </datalist>
{% endfor %}