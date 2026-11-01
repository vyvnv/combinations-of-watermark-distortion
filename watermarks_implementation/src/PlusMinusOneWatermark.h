#ifndef PLUS_MINUS_ONE_WATERMARK_H_
#define PLUS_MINUS_ONE_WATERMARK_H_

#include "Watermark.h"

class PlusMinusOneWatermark : public Watermark
{
public:
	PlusMinusOneWatermark(double detectThreshold = -1, const std::vector<std::size_t> positions = std::vector<std::size_t>(), std::vector<bool> reference = std::vector<bool>(), std::vector<bool> b = std::vector<bool>());
	void setDetectThreshold(double detectThreshold);

	bool embed(std::shared_ptr<VideoFrame> pframe, bool value);
	DetectResult detect(const std::shared_ptr<VideoFrame> pframe);

	static std::vector<std::size_t> createPositions(const std::shared_ptr<VideoFrame> &pframe, int count);
	static std::vector<bool> createReference(int count); //createReference used for both reference and b vectors 

	static void store(const std::vector<std::size_t> &positions, const std::vector<bool> &reference, const std::vector<bool>&b, const std::string& filename);
	static bool load(const std::string& filename, std::vector<std::size_t>& positions, std::vector<bool>& reference, std::vector<bool>& b);

private:
	double                       m_detectThreshold;
	std::vector<bool>            m_reference;
	std::vector<bool>            m_b;
	std::vector<std::size_t>     m_positions;
};

#endif
