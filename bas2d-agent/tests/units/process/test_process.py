import simplejpeg

from app.process.encoding import EncodingProcess


def test_should_return_simplejpeg(mock_image):
    # given
    encoder = EncodingProcess()

    # when
    data = encoder.process(mock_image)

    # then
    assert simplejpeg.is_jpeg(data), "data should be jpeg type"
