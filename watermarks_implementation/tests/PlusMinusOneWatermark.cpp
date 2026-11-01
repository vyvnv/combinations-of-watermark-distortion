#include <boost/test/unit_test.hpp>

#include <memory>

#include "Utils.h"
#include "VideoFrame.h"
#include "PlusMinusOneWatermark.h"

BOOST_AUTO_TEST_SUITE(plusminusone_watermark);

/*BOOST_AUTO_TEST_CASE(plusminusone_positions)
{
  std::shared_ptr<VideoFrame> pframe = std::make_shared<VideoFrame>(getSourceDir(__FILE__) + "images/sea_640.jpg", VideoFrame::Grayscale);

  BOOST_CHECK_EQUAL(pframe->width(), 480);
  BOOST_CHECK_EQUAL(pframe->height(), 640);

  std::vector<std::size_t> positions = PlusMinusOneWatermark::createPositions(pframe, 10000);

  std::size_t maxPosition = 640 * 480;

  for (std::size_t i = 0; i < positions.size(); i++)
  {
    BOOST_CHECK(positions[i] < maxPosition);
    //add code for duplicating and out of range positions checking
  }
}

BOOST_AUTO_TEST_CASE(plusminusone_positions_color)
{
  std::shared_ptr<VideoFrame> pframe = std::make_shared<VideoFrame>(getSourceDir(__FILE__) + "images/sea_640.jpg", VideoFrame::Color);

  BOOST_CHECK_EQUAL(pframe->width(), 480);
  BOOST_CHECK_EQUAL(pframe->height(), 640);

  std::vector<std::size_t> positions = PlusMinusOneWatermark::createPositions(pframe, 10000);

  std::size_t maxPosition = 640 * 480;

  for (std::size_t i = 0; i < positions.size(); i++)
  {
    BOOST_CHECK(positions[i] < maxPosition);
    //add code for duplicating and out of range positions checking for color images(3*480*640)
  }
}

BOOST_AUTO_TEST_CASE(plusminusone_load_store)
{
  std::shared_ptr<VideoFrame> pframe = std::make_shared<VideoFrame>(getSourceDir(__FILE__) + "images/sea_640.jpg", VideoFrame::Color);

  BOOST_CHECK_EQUAL(pframe->width(), 480);
  BOOST_CHECK_EQUAL(pframe->height(), 640);

  std::vector<std::size_t> positions = PlusMinusOneWatermark::createPositions(pframe, 10000);
  std::vector<bool> reference = PlusMinusOneWatermark::createReference(10000);
  std::vector<bool> b = PlusMinusOneWatermark::createReference(10000);


  PlusMinusOneWatermark::store(positions, reference, b, getSourceDir(__FILE__) + "out/plusminusone_load_store");

  std::vector<std::size_t> positionsLoaded = PlusMinusOneWatermark::createPositions(pframe, 10000);
  std::vector<bool> referenceLoaded = PlusMinusOneWatermark::createReference(10000);
  std::vector<bool> bLoaded = PlusMinusOneWatermark::createReference(10000);

  PlusMinusOneWatermark::load(getSourceDir(__FILE__) + "out/plusminusone_load_store", positionsLoaded, referenceLoaded, bLoaded);

  BOOST_CHECK_EQUAL(positions.size(), positionsLoaded.size());
  bool collections_equal = true;
  for (size_t i = 0; i < positions.size() && collections_equal; i++)
  {
    if(positions[i] != positionsLoaded[i])
      collections_equal = false;
  }

  BOOST_CHECK_EQUAL(reference.size(), referenceLoaded.size());
  for (size_t i = 0; i < reference.size() && collections_equal; i++)
  {
    if (reference[i] != referenceLoaded[i])
      collections_equal = false;
  }

  BOOST_CHECK_EQUAL(b.size(), bLoaded.size());
  for (size_t i = 0; i < b.size() && collections_equal; i++)
  {
    if (b[i] != bLoaded[i])
      collections_equal = false;
  }


  BOOST_CHECK(collections_equal);
}

BOOST_AUTO_TEST_CASE(plusminusone_watermark)
{
  std::shared_ptr<VideoFrame> pframe = std::make_shared<VideoFrame>(getSourceDir(__FILE__) + "images/sea_640.jpg", VideoFrame::Grayscale);
  std::shared_ptr<VideoFrame> pframeTrue = std::make_shared<VideoFrame>(*pframe);

  BOOST_CHECK_EQUAL(pframe->width(), 480);
  BOOST_CHECK_EQUAL(pframe->height(), 640);

  std::vector<bool> reference = PlusMinusOneWatermark::createReference(10000);
  std::vector<bool> b = PlusMinusOneWatermark::createReference(10000);
  std::vector<std::size_t> positions = PlusMinusOneWatermark::createPositions(pframe, 10000);

  PlusMinusOneWatermark watermark(0.5, positions, reference, b);
  watermark.embed(pframeTrue, true);

  BOOST_CHECK_EQUAL(watermark.detect(pframeTrue), Watermark::DetectResult::TRUE);
  BOOST_CHECK_EQUAL(watermark.detect(pframe), Watermark::DetectResult::NO_WATERMARK);
}
*/

BOOST_AUTO_TEST_SUITE_END();
