#include <boost/test/unit_test.hpp>

#include <memory>

#include "Utils.h"
#include "VideoFrame.h"
#include "EBlindDLC_DctDniz_Robust.h"

BOOST_AUTO_TEST_SUITE(eblind_dlc_dct_dniz_robust);

BOOST_AUTO_TEST_CASE(embed_detect)
{
  std::shared_ptr<VideoFrame> pframe = std::make_shared<VideoFrame>(getSourceDir(__FILE__) + "images/sea_640.jpg", VideoFrame::Grayscale);

  BOOST_CHECK_EQUAL(pframe->width(), 480);
  BOOST_CHECK_EQUAL(pframe->height(), 640);

  std::shared_ptr<VideoFrame> pframeTrue = std::make_shared<VideoFrame>(*pframe);

  auto preference = EBlindDLC_DctDniz_Robust::createReference(pframe, 255, 10);

  EBlindDLC_DctDniz_Robust watermark(0.3, 0.1, preference);
  watermark.embed(pframeTrue, true);

  double correlationEmbedded = 0;
  watermark.getCorrelation(pframeTrue, correlationEmbedded);
  double correlationNonEmbedded = 0;
  watermark.getCorrelation(pframe, correlationNonEmbedded);

  BOOST_CHECK_GE(correlationEmbedded, correlationNonEmbedded);

  EBlindDLC_DctDniz_Robust watermarkDetect(0.3, (correlationEmbedded + correlationNonEmbedded) / 2, preference);


  BOOST_CHECK_EQUAL(watermarkDetect.detect(pframe), Watermark::DetectResult::NO_WATERMARK);
  BOOST_CHECK_EQUAL(watermarkDetect.detect(pframeTrue), Watermark::DetectResult::TRUE);
}

BOOST_AUTO_TEST_SUITE_END();
