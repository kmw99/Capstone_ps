import cv2
import numpy as np
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QOpenGLFunctions
from PySide6.QtGui import QImage
from PySide6.QtOpenGL import QOpenGLTexture, QOpenGLShaderProgram, QOpenGLShader
from OpenGL.GL import GL_TRIANGLE_STRIP

class OpenGLVideoRenderer(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame = None
        self.texture = None
        self.program = None

    def set_frame(self, frame: np.ndarray):
        if frame is None:
            return
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.update()

    def initializeGL(self):
        self.gl = self.context().functions()
        self.program = QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, """
            attribute vec2 position;
            attribute vec2 texcoord;
            varying vec2 v_texcoord;
            void main() {
                gl_Position = vec4(position, 0.0, 1.0);
                v_texcoord = texcoord;
            }
        """)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, """
            uniform sampler2D texture;
            varying vec2 v_texcoord;
            void main() {
                gl_FragColor = texture2D(texture, v_texcoord);
            }
        """)
        self.program.link()

    def paintGL(self):
        if self.frame is None:
            return

        h, w, _ = self.frame.shape
        image = QImage(self.frame.data, w, h, QImage.Format_RGB888)
        if self.texture:
            self.texture.destroy()

        self.texture = QOpenGLTexture(image)
        self.texture.setMinMagFilters(QOpenGLTexture.Linear, QOpenGLTexture.Linear)

        self.texture.bind()
        self.program.bind()

        vertices = np.array([
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,
             1.0,  1.0
        ], dtype=np.float32)

        texcoords = np.array([
            0.0, 1.0,
            1.0, 1.0,
            0.0, 0.0,
            1.0, 0.0
        ], dtype=np.float32)

        self.program.enableAttributeArray("position")
        self.program.setAttributeArray("position", vertices, 2)

        self.program.enableAttributeArray("texcoord")
        self.program.setAttributeArray("texcoord", texcoords, 2)

        self.gl.glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        self.program.disableAttributeArray("position")
        self.program.disableAttributeArray("texcoord")
        self.program.release()
        self.texture.release()

    def resizeGL(self, w, h):
        self.glViewport(0, 0, w, h)