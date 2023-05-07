# Autogenerated file
def render(marks, disabled):
    yield """<!DOCTYPE html>
<html>
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Pico W</title>
    <link rel=\"stylesheet\" href=\"bulma.min.css\">
  </head>
  <body>
    <div class=\"container is-fluid is-mobile is-centered\">
      <section class=\"columns \">
        <div class=\"column\"></div>

        <div class=\"column\">

          <div class=\"level\">
            <div class=\"level-item has-text-centered\">
              <figure class=\"image is-128x128\">
                <img src=\"computer.svg\" alt=\"Pico W Icon\" />
              </figure>
            </div>
          </div>

          <form class=\"box\" action=\"\" method=\"POST\">

            <div class=\"level\">
              <div class=\"level-item has-text-centered\">
                <div class=\"columns\">
                  <div class=\"field is-grouped\">
                    <div class=\"field-body\">
                      <div class=\"field\">
                        <div class=\"control\">

                          <div class=\"column\">
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"00\" """
    yield str(disabled [0][0])
    yield """>
                              """
    yield str(marks[0][0])
    yield """
                            </label>
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"01\" """
    yield str(disabled [0][1])
    yield """>
                              """
    yield str(marks[0][1])
    yield """
                            </label>
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"02\" """
    yield str(disabled [0][2])
    yield """>
                              """
    yield str(marks[0][2])
    yield """
                            </label>
                          </div>


                          <div class=\"column\">
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"10\" """
    yield str(disabled [1][0])
    yield """>
                              """
    yield str(marks[1][0])
    yield """
                            </label>
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"11\" """
    yield str(disabled [1][1])
    yield """>
                              """
    yield str(marks[1][1])
    yield """
                            </label>
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"12\" """
    yield str(disabled [1][2])
    yield """>
                              """
    yield str(marks[1][2])
    yield """
                            </label>
                          </div>

                          <div class=\"column\">
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"20\" """
    yield str(disabled [2][0])
    yield """>
                              """
    yield str(marks[2][0])
    yield """
                            </label>
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"21\" """
    yield str(disabled [2][1])
    yield """>
                              """
    yield str(marks[2][1])
    yield """
                            </label>
                            <label class=\"radio\">
                              <input type=\"radio\" name=\"square\" value=\"22\" """
    yield str(disabled [2][2])
    yield """>
                              """
    yield str(marks[2][2])
    yield """
                            </label>
                          </div>

                        </div>
                      </div>
                    </div>

                  </div>
                </div>


              </div>
            </div>
                    <div class=\"control\">
                      <input class=\"button is-primary\" type=\"submit\" value=\"Mark!\">
                    </div>
          </form>

          <div class=\"column auto\"></div>

        </section>
      </div>

  </body>
</html>
"""
