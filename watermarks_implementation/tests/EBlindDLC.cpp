#include <boost/test/unit_test.hpp>

#include <memory>

#include "Utils.h"
#include "VideoFrame.h"
#include "EBlindDLC.h"

BOOST_AUTO_TEST_SUITE(eblind_dlc);

BOOST_AUTO_TEST_CASE(embed_detect)
{
  std::shared_ptr<VideoFrame> pframe = std::make_shared<VideoFrame>(getSourceDir(__FILE__) + "images/sea_640.jpg", VideoFrame::Grayscale);

  BOOST_CHECK_EQUAL(pframe->width(), 480);
  BOOST_CHECK_EQUAL(pframe->height(), 640);

  std::shared_ptr<VideoFrame> pframeTrue = std::make_shared<VideoFrame>(*pframe);

  auto preference = EBlindDLC::createReference(pframe);

  EBlindDLC watermark(25.0, 0.000001, preference, Detector::CORRELATION_COEFFICIENT);
  watermark.embed(pframeTrue, true);

  BOOST_CHECK_EQUAL(watermark.detect(pframe), Watermark::DetectResult::NO_WATERMARK);
  BOOST_CHECK_EQUAL(watermark.detect(pframeTrue), Watermark::DetectResult::TRUE);
}

BOOST_AUTO_TEST_SUITE_END();
