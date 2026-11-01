#include "VideoFrame.h"
#include "WatermarkReference.h"
#include "Detector.h"
#include "DCTWatermark.h"
#include "VideoFrameBlockProcessor.h"

#include <boost/program_options.hpp>
#include "boost/property_tree/ptree.hpp"
#include <boost/property_tree/json_parser.hpp>

#include <opencv2/opencv.hpp>

#include <iostream>

using boost::property_tree::ptree;

class SerializeItem
{
public:
	SerializeItem(std::size_t itemLength)
	{
		coefficients.resize(itemLength);
		watermark.resize(itemLength);
	}
	std::vector<double> coefficients;
	std::vector<double> watermark;
	bool value;
	std::size_t block_idx;
};


ptree vectorToPtree(const std::vector<double>& vec)
{
	ptree pt;

	std::ostringstream oss;
	for (size_t i = 0; i < vec.size(); ++i) 
	{
		if (i > 0) 
			oss << ",";
		oss << vec[i];
	}
	pt.put("", oss.str());
	return pt;
}

ptree serializeItemToPtree(const SerializeItem& item) 
{
	ptree item_node;
	item_node.add_child("coefficients", vectorToPtree(item.coefficients));
	item_node.add_child("watermark", vectorToPtree(item.watermark));
	item_node.put("value", item.value);
	return item_node;
}

ptree serializeVectorToPtree(const std::vector<SerializeItem>& items) 
{
	ptree root;
	for (const auto& item : items) 
		root.push_back(std::make_pair(std::to_string(item.block_idx), serializeItemToPtree(item)));

	return root;
}

int main(int argc, char** argv)
{
	namespace po = boost::program_options;

	po::options_description desc("Allowed options");
	desc.add_options()
		("help", "produce help message")
		("in,i", po::value<std::string>(), "input file")
		("reference,r", po::value<std::string>(), "reference file")
		("out,o", po::value<std::string>(), "output file")
		("value,v", po::value<bool>(), "embedding flag")
		("skip_count,s", po::value<int>()->default_value(16), "number of first coefficients to skip")
		;

	po::variables_map vm;
	po::store(po::parse_command_line(argc, argv, desc), vm);

	if (!vm.count("in") || !vm.count("out") || !vm.count("reference") || !vm.count("value") || vm.count("help"))
	{
		std::cout << desc << "\n";
		return 0;
	}

	std::shared_ptr<VideoFrame> pframe = std::make_shared<VideoFrame>(vm["in"].as<std::string>());
	if (!pframe)
	{
		std::cout << "Error opening input file `" + vm["in"].as<std::string>() + "`";
		return 1;
	}

	std::vector<double> referenceData = DCTWatermark::referenceLoad(vm["reference"].as<std::string>());
	if (referenceData.empty())
	{
		std::cout << "Error opening reference file `" + vm["reference"].as<std::string>() + "`";
		return 1;
	}

	int skipCount = vm["skip_count"].as<int>();

	VideoFrameBlockProcessor blockProcessor(pframe, DCTWatermark::BLOCK_SIZE);

	std::size_t expectedReferenceSize = blockProcessor.getBlockCount() * (DCTWatermark::BLOCK_SIZE * DCTWatermark::BLOCK_SIZE - skipCount);
	if (expectedReferenceSize != referenceData.size())
	{
		std::cout << "Wrong reference size";
		return 1;
	}

	std::vector<double> extractedData(expectedReferenceSize);
	std::size_t blockCount = blockProcessor.getBlockCount();
	std::size_t extractIdx = 0;
	double sumDCT = 0;
	for (std::size_t idx = 0; idx < blockCount; idx++)
	{
		std::vector<uint8_t> blockData = blockProcessor.getBlock(idx);

		std::vector<float> srcData(blockData.size());
		std::vector<float> dstData(blockData.size());
		for (int i = 0; i < blockData.size(); i++)
			srcData[i] = blockData[i];

		cv::Mat src = cv::Mat((int)DCTWatermark::BLOCK_SIZE, (int)DCTWatermark::BLOCK_SIZE, CV_32F, &srcData[0]);
		cv::Mat dst = cv::Mat((int)DCTWatermark::BLOCK_SIZE, (int)DCTWatermark::BLOCK_SIZE, CV_32F, &dstData[0]);

		cv::dct(src, dst);
		std::vector<float> zigzag = DCTWatermark::zigzagScan(dstData);

		for (std::size_t pos = skipCount; pos < DCTWatermark::BLOCK_SIZE * DCTWatermark::BLOCK_SIZE; pos++)
		{
			float val = zigzag[pos];
			extractedData[extractIdx] = val;
			extractIdx++;
		}
	}

	bool value = vm["value"].as<bool>();

	const int itemLength = DCTWatermark::BLOCK_SIZE * DCTWatermark::BLOCK_SIZE - skipCount;

	std::vector<SerializeItem> items;
	for (std::size_t idx = 0, block_idx=0; idx < extractedData.size(); idx += itemLength, block_idx++)
	{
		SerializeItem item(itemLength);

		std::copy(&extractedData.at(idx), &extractedData.at(idx) + itemLength, item.coefficients.begin());
		std::copy(&referenceData.at(idx), &referenceData.at(idx) + itemLength, item.watermark.begin());
		item.value = value;
		item.block_idx = block_idx;
		items.push_back(item);
	}

	ptree root = serializeVectorToPtree(items);
	boost::property_tree::write_json(vm["out"].as<std::string>(), root);

	return 0;
}
