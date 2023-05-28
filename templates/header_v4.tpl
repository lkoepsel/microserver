{% args leds%}
<table>
    <thead>
        <tr>
            <th colspan="2">LED Demo Pins</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Color</td>
            <th>Pico Pin</td>
        </tr>
        <tr>
            <td>{{ leds[0][0] }}</td>
            <td>{{ leds[0][1] }}</td>
        </tr>
        <tr>
            <td>{{ leds[1][0] }}</td>
            <td>{{ leds[1][1] }}</td>
        </tr>
        <tr>
            <td>{{ leds[2][0] }}</td>
            <td>{{ leds[2][1] }}</td>
        </tr>
        <tr>
            <td>{{ leds[3][0] }}</td>
            <td>{{ leds[3][1] }}</td>
        </tr>
    </tbody>
</table>
